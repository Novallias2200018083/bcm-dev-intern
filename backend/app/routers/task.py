import os
import uuid
import re
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core.database import get_db
from app.models.task import TaskPriority, TaskStatus
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
    TaskStatsResponse,
)
from app.crud import task as crud_task

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.get(
    "/stats",
    response_model=TaskStatsResponse,
    summary="Ringkasan Statistik Tugas",
    description="Mengembalikan statistik jumlah total tugas, tugas menunggu, dikerjakan, selesai, terlambat, dan persentase kelulusan.",
)
def get_stats(db: Session = Depends(get_db)):
    return crud_task.get_task_stats(db)

@router.get(
    "/categories",
    response_model=List[str],
    summary="Daftar Kategori",
    description="Mengembalikan daftar opsi kategori tugas harian.",
)
def get_categories(db: Session = Depends(get_db)):
    return crud_task.get_categories(db)

@router.get(
    "",
    response_model=List[TaskResponse],
    summary="Daftar Semua Tugas",
    description="Mengambil daftar tugas harian dengan filter pencarian, status, prioritas, kategori, deadline, dan pengurutan.",
)
def list_tasks(
    status: Optional[str] = Query(None, description="Filter berdasarkan status (pending, in_progress, completed, completed_on_time, completed_late)"),
    priority: Optional[TaskPriority] = Query(None, description="Filter berdasarkan prioritas"),
    category: Optional[str] = Query(None, description="Filter berdasarkan kategori"),
    search: Optional[str] = Query(None, description="Kata kunci pencarian (judul, deskripsi, atau kategori)"),
    is_overdue: Optional[bool] = Query(None, description="Filter hanya tugas yang lewat deadline dan belum selesai"),
    sort_by: str = Query("created_at", description="Kolom urutan (created_at, due_date, priority, title, status)"),
    order: str = Query("desc", description="Arah pengurutan (asc atau desc)"),
    skip: int = Query(0, ge=0, description="Offset data"),
    limit: int = Query(200, ge=1, le=500, description="Batas jumlah data per request"),
    db: Session = Depends(get_db),
):
    tasks = crud_task.get_tasks(
        db=db,
        status=status,
        priority=priority,
        category=category,
        search=search,
        is_overdue=is_overdue,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit,
    )
    return tasks

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Detail Tugas",
    description="Mengambil detail tugas harian berdasarkan ID.",
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tugas dengan ID {task_id} tidak ditemukan",
        )
    return task

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tambah Tugas Baru",
    description="Mencatat tugas harian baru ke dalam sistem.",
)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    return crud_task.create_task(db=db, task_in=task_in)

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Perbarui Tugas",
    description="Memperbarui data tugas harian yang ada.",
)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)):
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tugas dengan ID {task_id} tidak ditemukan",
        )
    return crud_task.update_task(db=db, db_task=task, task_in=task_in)

@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    summary="Ubah Status Tugas Cepat",
    description="Mengubah status tugas secara cepat (pending, in_progress, completed).",
)
def update_task_status(task_id: int, payload: TaskStatusUpdate, db: Session = Depends(get_db)):
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tugas dengan ID {task_id} tidak ditemukan",
        )
    return crud_task.update_task_status(db=db, db_task=task, new_status=payload.status)

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Hapus Tugas",
    description="Menghapus tugas harian secara permanen.",
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tugas dengan ID {task_id} tidak ditemukan",
        )
    # Remove attachment file if exists
    if task.attachment_url:
        _remove_attachment_file(task.attachment_url)
    crud_task.delete_task(db=db, db_task=task)
    return None

def _remove_attachment_file(attachment_url: str):
    try:
        filename = os.path.basename(attachment_url)
        filepath = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Warning: Failed to delete attachment file: {e}")

@router.post(
    "/{task_id}/upload",
    response_model=TaskResponse,
    summary="Unggah Dokumen / Gambar Lampiran",
    description="Mengunggah berkas gambar atau dokumen pendukung untuk tugas tertentu (Maks 10 MB).",
)
async def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tugas dengan ID {task_id} tidak ditemukan",
        )

    # Validate file size (10 MB max)
    content = await file.read()
    file_size = len(content)
    max_size = 10 * 1024 * 1024 # 10MB
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ukuran berkas melebihi batas maksimal 10 MB",
        )

    # Remove previous attachment if existed
    if task.attachment_url:
        _remove_attachment_file(task.attachment_url)

    # Sanitize original filename
    orig_name = file.filename or "attachment"
    clean_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", orig_name)
    unique_filename = f"{uuid.uuid4().hex[:10]}_{clean_name}"
    filepath = os.path.join(UPLOAD_DIR, unique_filename)

    with open(filepath, "wb") as f:
        f.write(content)

    task.attachment_url = f"/uploads/{unique_filename}"
    task.attachment_name = orig_name
    task.attachment_type = file.content_type or "application/octet-stream"
    task.attachment_size = file_size

    db.commit()
    db.refresh(task)
    return task

@router.delete(
    "/{task_id}/attachment",
    response_model=TaskResponse,
    summary="Hapus Lampiran Tugas",
    description="Menghapus berkas lampiran yang terasosiasi dengan tugas ini.",
)
def delete_attachment(task_id: int, db: Session = Depends(get_db)):
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tugas dengan ID {task_id} tidak ditemukan",
        )

    if task.attachment_url:
        _remove_attachment_file(task.attachment_url)
        task.attachment_url = None
        task.attachment_name = None
        task.attachment_type = None
        task.attachment_size = None
        db.commit()
        db.refresh(task)

    return task


from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.models.task import TaskPriority, TaskStatus

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Judul tugas")
    description: Optional[str] = Field(None, description="Detail deskripsi tugas")
    category: Optional[str] = Field("Umum", max_length=60, description="Kategori tugas (e.g. Pekerjaan, Rapat, Proyek)")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Tingkat prioritas (low, medium, high)")
    due_date: Optional[datetime] = Field(None, description="Tenggat waktu pengerjaan tugas")
    attachment_url: Optional[str] = Field(None, description="URL berkas lampiran pendukung")
    attachment_name: Optional[str] = Field(None, description="Nama asli berkas lampiran")
    attachment_type: Optional[str] = Field(None, description="Tipe MIME berkas lampiran")
    attachment_size: Optional[int] = Field(None, description="Ukuran berkas dalam bytes")

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Judul tugas tidak boleh kosong atau hanya berisi spasi")
        return clean

class TaskCreate(TaskBase):
    status: Optional[TaskStatus] = Field(default=TaskStatus.PENDING, description="Status tugas awal")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=60)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    attachment_url: Optional[str] = None
    attachment_name: Optional[str] = None
    attachment_type: Optional[str] = None
    attachment_size: Optional[int] = None

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            clean = v.strip()
            if not clean:
                raise ValueError("Judul tugas tidak boleh kosong")
            return clean
        return v

class TaskStatusUpdate(BaseModel):
    status: TaskStatus = Field(..., description="Status baru tugas")

class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskStatsResponse(BaseModel):
    total: int
    pending: int
    in_progress: int
    completed: int
    completed_on_time: int
    completed_late: int
    overdue: int
    completion_rate: float


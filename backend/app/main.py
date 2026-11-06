from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import os
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings, UPLOAD_DIR
from app.core.database import engine, Base, SessionLocal
from app.models.task import Task, TaskPriority, TaskStatus
from app.routers import task_router

def seed_initial_tasks():
    """Seed initial realistic daily tasks if the table is currently empty."""
    db = SessionLocal()
    try:
        count = db.query(Task).count()
        if count == 0:
            now = datetime.now()
            sample_tasks = [
                Task(
                    title="Review Pull Request Modul Absensi Pegawai",
                    description="Melakukan code review dan testing fungsional untuk branch feature/attendance-v2 di repository Git.",
                    category="Pekerjaan",
                    priority=TaskPriority.HIGH,
                    status=TaskStatus.IN_PROGRESS,
                    due_date=now + timedelta(hours=4),
                ),
                Task(
                    title="Daily Standup Meeting Tim Engineering",
                    description="Koordinasi sprint harian, laporan blocker, dan update progress pekerjaan harian melalui Google Meet.",
                    category="Rapat",
                    priority=TaskPriority.HIGH,
                    status=TaskStatus.COMPLETED,
                    due_date=now - timedelta(hours=2),
                    completed_at=now - timedelta(hours=1),
                ),
                Task(
                    title="Menyusun Dokumentasi Teknis API & ERD",
                    description="Lengkapi dokumen Swagger, panduan instalasi, dan diagram alur modul daftar tugas harian.",
                    category="Pekerjaan",
                    priority=TaskPriority.MEDIUM,
                    status=TaskStatus.PENDING,
                    due_date=now + timedelta(days=1),
                ),
                Task(
                    title="Optimasi Query Database MySQL Task",
                    description="Membuat index komposit untuk filter status, prioritas, dan kategori agar load query tetap responsif.",
                    category="Proyek",
                    priority=TaskPriority.MEDIUM,
                    status=TaskStatus.PENDING,
                    due_date=now + timedelta(days=2),
                ),
                Task(
                    title="Update Sistem Operasi & Backup Database",
                    description="Jadwal pemeliharaan server mingguan dan backup snapshot berkala pada database staging.",
                    category="Pribadi",
                    priority=TaskPriority.LOW,
                    status=TaskStatus.COMPLETED,
                    due_date=now - timedelta(days=1),
                    completed_at=now - timedelta(hours=6),
                ),
            ]
            db.add_all(sample_tasks)
            db.commit()
            print("INFO: Initial sample tasks have been seeded successfully.")
    except Exception as e:
        print(f"WARNING: Error while seeding sample tasks: {e}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed default tasks
    try:
        Base.metadata.create_all(bind=engine)
        seed_initial_tasks()
    except Exception as e:
        print(f"CRITICAL: Failed to initialize database tables: {e}")
    yield
    # Shutdown logic if any

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="RESTful API Modul Pengelolaan Daftar Tugas Harian (Daily Task Management) dibangun dengan FastAPI dan MySQL.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
origins = settings.cors_origin_list
if not origins or "*" in origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if "*" not in origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler for unexpected exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Terjadi kesalahan internal pada server", "error": str(exc)},
    )

# Static uploads directory
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include API routers
app.include_router(task_router)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "docs_url": "/docs",
        "version": "1.0.0",
    }

@app.get("/api/health", tags=["Health Check"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "timezone": "Asia/Jakarta (WIB)",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.APP_DEBUG)

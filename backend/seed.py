import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from datetime import datetime, timedelta
from app.core.database import SessionLocal, Base, engine
from app.models.task import Task, TaskPriority, TaskStatus

def run_seed():
    print("Creating tables if not exists...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
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
        print(f"Success! {len(sample_tasks)} sample tasks inserted.")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()


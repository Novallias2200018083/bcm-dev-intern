import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, func
from app.core.database import Base

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(60), nullable=False, default="Umum", index=True)
    priority = Column(
        Enum(TaskPriority, values_callable=lambda obj: [e.value for e in obj], native_enum=False, length=20),
        default=TaskPriority.MEDIUM,
        nullable=False,
    )
    status = Column(
        Enum(TaskStatus, values_callable=lambda obj: [e.value for e in obj], native_enum=False, length=20),
        default=TaskStatus.PENDING,
        nullable=False,
        index=True,
    )
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    attachment_url = Column(String(500), nullable=True)
    attachment_name = Column(String(255), nullable=True)
    attachment_type = Column(String(100), nullable=True)
    attachment_size = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def mark_completed(self):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

    def mark_uncompleted(self, status: TaskStatus = TaskStatus.PENDING):
        self.status = status
        self.completed_at = None


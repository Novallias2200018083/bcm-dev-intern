from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, case
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatsResponse

def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    """Retrieve a single task by its primary key ID."""
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[TaskPriority] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_overdue: Optional[bool] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    skip: int = 0,
    limit: int = 200,
) -> List[Task]:
    """
    Retrieve tasks with dynamic filtering, full-text like searching, and sorting.
    """
    query = db.query(Task)

    # Filter by status (supports completed_on_time and completed_late)
    if status is not None and str(status).strip():
        s = str(status).strip()
        if s == "completed_on_time":
            query = query.filter(
                Task.status == TaskStatus.COMPLETED,
                or_(
                    Task.due_date.is_(None),
                    Task.completed_at.is_(None),
                    Task.completed_at <= Task.due_date,
                ),
            )
        elif s == "completed_late":
            query = query.filter(
                Task.status == TaskStatus.COMPLETED,
                Task.due_date.isnot(None),
                Task.completed_at.isnot(None),
                Task.completed_at > Task.due_date,
            )
        elif s in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED]:
            query = query.filter(Task.status == s)

    # Filter by Priority
    if priority is not None:
        query = query.filter(Task.priority == priority)

    # Filter by Category (Case-insensitive)
    if category is not None and category.strip():
        query = query.filter(func.lower(Task.category) == category.strip().lower())

    # Filter by overdue flag using local time
    now = datetime.now()
    if is_overdue is True:
        query = query.filter(
            Task.status != TaskStatus.COMPLETED,
            Task.due_date.isnot(None),
            Task.due_date < now
        )

    # Search keyword in title or description
    if search is not None and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Task.title.ilike(term),
                Task.description.ilike(term),
                Task.category.ilike(term),
            )
        )

    # Sorting
    valid_sort_fields = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "title": Task.title,
        "status": Task.status,
    }
    sort_column = valid_sort_fields.get(sort_by, Task.created_at)

    if order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.offset(skip).limit(limit).all()

def get_task_stats(db: Session) -> TaskStatsResponse:
    """
    Calculate real-time aggregated statistics for tasks dashboard.
    """
    now = datetime.now()
    
    stats = db.query(
        func.count(Task.id).label("total"),
        func.sum(case((Task.status == TaskStatus.PENDING, 1), else_=0)).label("pending"),
        func.sum(case((Task.status == TaskStatus.IN_PROGRESS, 1), else_=0)).label("in_progress"),
        func.sum(case((Task.status == TaskStatus.COMPLETED, 1), else_=0)).label("completed"),
        func.sum(
            case(
                (
                    (Task.status == TaskStatus.COMPLETED)
                    & (
                        (Task.due_date.is_(None))
                        | (Task.completed_at.is_(None))
                        | (Task.completed_at <= Task.due_date)
                    ),
                    1,
                ),
                else_=0,
            )
        ).label("completed_on_time"),
        func.sum(
            case(
                (
                    (Task.status == TaskStatus.COMPLETED)
                    & (Task.due_date.isnot(None))
                    & (Task.completed_at.isnot(None))
                    & (Task.completed_at > Task.due_date),
                    1,
                ),
                else_=0,
            )
        ).label("completed_late"),
        func.sum(
            case(
                (
                    (Task.status != TaskStatus.COMPLETED) & (Task.due_date.isnot(None)) & (Task.due_date < now),
                    1,
                ),
                else_=0,
            )
        ).label("overdue"),
    ).first()

    total = stats.total or 0
    pending = stats.pending or 0
    in_progress = stats.in_progress or 0
    completed = stats.completed or 0
    completed_on_time = stats.completed_on_time or 0
    completed_late = stats.completed_late or 0
    overdue = stats.overdue or 0
    completion_rate = round((completed / total * 100), 1) if total > 0 else 0.0

    return TaskStatsResponse(
        total=total,
        pending=pending,
        in_progress=in_progress,
        completed=completed,
        completed_on_time=completed_on_time,
        completed_late=completed_late,
        overdue=overdue,
        completion_rate=completion_rate,
    )

def get_categories(db: Session) -> List[str]:
    """Retrieve distinct category list."""
    rows = db.query(Task.category).distinct().order_by(Task.category.asc()).all()
    categories = [r[0] for r in rows if r[0]]
    defaults = ["Umum", "Pekerjaan", "Rapat", "Proyek", "Pribadi"]
    # Merge and preserve order
    merged = list(dict.fromkeys(defaults + categories))
    return merged

def create_task(db: Session, task_in: TaskCreate) -> Task:
    """Create a new task."""
    task_data = task_in.model_dump()
    
    # If created directly as completed, set completed_at timestamp
    if task_data.get("status") == TaskStatus.COMPLETED:
        task_data["completed_at"] = datetime.now()

    db_task = Task(**task_data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    """Update task fields."""
    update_data = task_in.model_dump(exclude_unset=True)

    for field, val in update_data.items():
        if field == "status" and val is not None:
            if val == TaskStatus.COMPLETED and db_task.status != TaskStatus.COMPLETED:
                db_task.completed_at = datetime.now()
            elif val != TaskStatus.COMPLETED:
                db_task.completed_at = None
            setattr(db_task, field, val)
        else:
            setattr(db_task, field, val)

    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, db_task: Task, new_status: TaskStatus) -> Task:
    """Quickly toggle/update task status."""
    if new_status == TaskStatus.COMPLETED:
        db_task.mark_completed()
    else:
        db_task.mark_uncompleted(new_status)

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, db_task: Task) -> None:
    """Delete a task permanently."""
    db.delete(db_task)
    db.commit()

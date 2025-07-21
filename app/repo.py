from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Task, TaskComment, TaskState


def get_task(db: Session, task_id: str) -> Task | None:
    return db.get(Task, task_id)


def create_task(db: Session, descr: str) -> Task:
    task = Task(descr=descr)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, 
                task_id: int, 
                descr: str | None = None, 
                status: int | None = None, 
                assigned_to: str | None = None) -> Task | None:
    task = db.get(Task, task_id)
    if not task:
        return None

    # NOTE: setattr() for attribute list
    if descr is not None:
        task.descr = descr
    if status is not None:
        task.status = status
    if assigned_to is not None:
        task.assigned_to = assigned_to
    
    db.commit()
    db.refresh(task)
    return task


def tasklist(db: Session) -> list[Task]:
    return db.execute(select(Task)).scalars().all()


def post_comment(db: Session, task_id: int, text: str) -> TaskComment | None:
    task = db.get(Task, task_id)
    if not task:
        return None
    comment = TaskComment(task_id=task_id, text=text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def task_comments(db: Session, task_id: int) -> list[TaskComment] | None:
    task = db.get(Task, task_id)
    if not task:
        return None
    stmt = select(TaskComment).where(TaskComment.task_id == task_id)
    comments = db.execute(stmt).scalars().all()
    return comments

import logging
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.repo

logger = logging.getLogger(__name__)


### NOTE: schemas

class TaskResponse(BaseModel):
    id: int
    descr: str
    status: int
    assigned_to: str | None

    class Config:
        from_attributes = True


class TaskCreateResponse(BaseModel):
    id: int
    descr: str
    status: int
    assigned_to: str | None

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]

    class Config:
        from_attributes = True


class TaskCommentResponse(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True


class TaskCommentsResponse(BaseModel):
    comments: list[TaskCommentResponse]

    class Config:
        from_attributes = True


class CreateTaskRequest(BaseModel):
    id: int
    descr: str


class UpdateTaskRequest(BaseModel):
    id: int
    descr: str | None
    status: int | None


class AssignTaskRequest(BaseModel):
    id: int
    user_id: str


class CommentTaskRequest(BaseModel):
    id: int
    text: str

###


router = APIRouter()


# NOTE: implement 404 as middleware

TASK_NOT_FOUND = HTTPException(status_code=404, detail="Task not found")


@router.get("/tasklist", tags=["task"], response_model=TaskListResponse)
def tasklist(db: Session = Depends(get_db)):
    tasks = repo.tasklist(db)
    return TaskListResponse(tasks=tasks)


@router.get("/task/{task_id}", tags=["task"], response_model=TaskResponse)
def task_info(task_id: int, db: Session = Depends(get_db)):
    logger.debug("task_info:", task_id=task_id)
    if task := repo.get_task(db, task_id):
        return TaskResponse(**task)
    raise TASK_NOT_FOUND


@router.post("/task", tags=["task"], response_model=TaskCreateResponse)
def create_task(descr: str, db: Session = Depends(get_db)):
    logger.debug("create_task:")
    task = repo.create_task(db, descr)
    return TaskCreateResponse(**task)


@router.put("/task/{task_id}", tags=["task"], response_model=TaskResponse)
def update_task(task_id: int, descr: str, db: Session = Depends(get_db)):
    task = repo.update_task(db, task_id, descr=descr)
    if task:
        return TaskResponse(**task)
    raise TASK_NOT_FOUND


@router.put("/task/{task_id}/assign", tags=["task"], response_model=TaskResponse)
def assign_task(task_id: int, user_id: str, db: Session = Depends(get_db)):
    task = repo.update_task(db, task_id, assigned_to=user_id)
    if task:
        return TaskResponse(**task)
    raise TASK_NOT_FOUND


@router.post("/task/{task_id}/comment", tags=["task", "comment"], response_model=TaskCommentResponse)
def comment_task(task_id: int, text: str, db: Session = Depends(get_db)):
    comment = repo.post_comment(db, task_id=task_id, text=text)
    if comment is not None:
        return TaskCommentResponse(**comment)
    raise TASK_NOT_FOUND


@router.get("/task/{task_id}/comments", tags=["task", "comment"], response_model=TaskCommentsResponse)
def task_comments(task_id: int, db: Session = Depends(get_db)):
    comments = repo.task_comments(db, task_id)
    if comments is not None:
        return TaskCommentsResponse(comments=[TaskCommentResponse(**c) for c in comments])
    return TASK_NOT_FOUND

import logging
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


class TaskResponse(BaseModel):
    task_id: str
    task_text: str


@router.get("/task/{task_id}", tags=["task"], response_model=TaskResponse)
def task_info(task_id: str):
    logger.debug("task_info:", task_id=task_id)
    # if found()
    return TaskResponse(task_id, "??? task text ???")


class CreateTask(BaseModel):
    task_id: str
    text: Optional[str] = ""


@router.post("/task", tags=["task"])
def create_task(task_id: str, descr: str):
    logger.debug("create_task:", task_id=task_id)
    return dict(task_id=task_id, task_name="??? name ???")


@router.put("/task/{task_id}", tags=["task"])
def update_task(task_id: str, descr: str):
    ...


@router.put("/task/{task_id}/assign", tags=["task"])
def assign_task(task_id: str, user_id: str):
    ...


@router.post("/task/{task_id}/comment", tags=["task", "comment"])
def comment_task(task_id: str, text: str):
    ...


@router.get("/task/{task_id}/comments", tags=["task", "comment"])
def task_comments(task_id: str) -> list[TaskComment]:
    ...

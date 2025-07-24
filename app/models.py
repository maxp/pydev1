from enum import IntEnum
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TaskState(IntEnum):
    ACTIVE = 1
    CLOSED = 2


class Task(Base):
    __tablename__ = "tasks"

    id:     Mapped[int] = mapped_column(primary_key=True)
    descr:  Mapped[str] = mapped_column(String(4000))
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=TaskState.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    assigned_to: Mapped[str | None] = mapped_column(String(100)) # NOTE: external reference scope
   
    comments: Mapped[list["TaskComment"]] = relationship(
        "TaskComment", 
        back_populates="task", 
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, status='{self.status}', assigned_to='{self.assigned_to}')>"


class TaskComment(Base):
    __tablename__ = "comments"

    id:   Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String(4000))
    # user_id: field not yet implemented
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    task: Mapped["Task"] = relationship("Task", back_populates="comments")


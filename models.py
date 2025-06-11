from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, Column
from datetime import date, datetime
from typing import Optional, List, Type, Dict, Any
from enum import Enum
from sqlalchemy import Enum as SQLEnum
# --- Models ---

# 1) Define your Python enum
class PriorityEnum(str, Enum):
    LOW    = "Low"
    MEDIUM = "Medium"
    HIGH   = "High"
    URGENT = "Urgent"

class StatusEnum(str, Enum):
    WISH_LIST = "Wish List"
    BACKLOG    = "Backlog"
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    IN_REVIEW = "In Review"
    REWORKED = "Reworked"
    COMPLETED   = "Completed"
    ON_HOLD     = "On Hold"
    ARCHIVED    = "Archived"

class Priority(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # this column can only ever be one of the four values above
    level: PriorityEnum = Field(
        sa_column=Column(
            SQLEnum(PriorityEnum, name="priorityenum"),  # Postgres, SQLite, etc.
            nullable=False,
            default=PriorityEnum.MEDIUM
        )
    )

    # back-ref to tasks
    tasks: List["Task"] = Relationship(back_populates="priority")

class Status(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # this column can only ever be one of the four values above
    level: StatusEnum = Field(
        sa_column=Column(
            SQLEnum(StatusEnum, name="statusenum"),  # Postgres, SQLite, etc.
            nullable=False,
            default=StatusEnum.BACKLOG
        )
    )

    # back-ref to tasks
    tasks: List["Task"] = Relationship(back_populates="status")

class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    height: float
    tasks: List["Task"] = Relationship(back_populates="person")

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="project")
    status_id: Optional[int] = Field(default=None, foreign_key="status.id")
    priority_id: Optional[int] = Field(default=None, foreign_key="priority.id")

class TaskTagLink(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = Field(default=False)
    time_on_task: Optional[float] = Field(default=None, nullable=True)

    person_id: Optional[int] = Field(default=None, foreign_key="person.id")
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    priority_id: Optional[int] = Field(default=None, foreign_key="priority.id")
    status_id: Optional[int] = Field(default=None, foreign_key="status.id")

    # Relationships
    person: Optional["Person"] = Relationship(back_populates="tasks")
    project: Optional["Project"]  = Relationship(back_populates="tasks")
    priority: Optional[Priority] = Relationship(back_populates="tasks")
    status: Optional[Status] = Relationship(back_populates="tasks")
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTagLink)



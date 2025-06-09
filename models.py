from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from datetime import date, datetime
from typing import Optional, List
# --- Models ---
class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    height: float

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="project")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = Field(default=False)
    time_on_task: Optional[float] = Field(default=None, nullable=True)
    person_id: Optional[int] = Field(default=None, foreign_key="person.id")
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")

    project: Optional["Project"]  = Relationship(back_populates="tasks")
from typing import Type
from sqlmodel import select, SQLModel
from setup_database import get_session

from models import Person, Task

# @solara.cache(ttl=300)
def load_people() -> list[Person]:
    with get_session() as sess:
        return list(sess.exec(select(Person)).all())

def load_all_database_items(model: Type[SQLModel]) -> list[SQLModel]:
    with get_session() as sess:
        return list(sess.exec(select(model)).all())


# @solara.cache(ttl=300)
def load_tasks(person_id: int | None = None) -> list[Task]:
    select_task = select(Task)
    if person_id is None:
        select_task = select_task.where(Task.person_id.is_(None))
    else:
        select_task = select_task.where(Task.person_id == person_id)

    with get_session() as sess:
        return list(sess.exec(select_task).all())
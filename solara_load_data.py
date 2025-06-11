from solara.server.settings import session
from sqlmodel import select

from main import get_session
from models import Person, Task

# @solara.cache(ttl=300)
def load_people() -> list[Person]:
    with get_session() as sess:
        return list(sess.exec(select(Person)).all())


# @solara.cache(ttl=300)
def load_tasks(person_id: int | None = None) -> list[Task]:
    selectTask = select(Task)
    if person_id is None:
        selectTask = selectTask.where(Task.person_id.is_(None))
    else:
        selectTask = selectTask.where(Task.person_id == person_id)

    with get_session() as sess:
        return list(sess.exec(selectTask).all())
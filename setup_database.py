from sqlmodel import SQLModel, create_engine, Session
from models import Person, Task
from sqlalchemy.engine import Engine

def create_db_and_tables(sqlite_file_path: str = "my_app.db") -> Engine:
    database_url = f"sqlite:///{sqlite_file_path}"
    engine = create_engine(database_url, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine

def insert_sample_data(engine) -> None:
    with Session(engine) as session:
        person = Person(name="John Doe", age=30, height=5.9)
        session.add(person)
        session.commit()
        session.refresh(person)

        task = Task(title="Sample Task", description="This is a sample task.", person_id=person.id)
        session.add(task)
        session.commit()
        session.refresh(task)
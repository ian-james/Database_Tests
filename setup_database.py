import os
from typing import Type, Dict, Any

from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    url =  os.getenv("DATABASE_URL")
    print(url)
    new_engine = create_engine(
        url,
        connect_args={"check_same_thread": False},
        echo=False,
    )
    # runs only once per session
    SQLModel.metadata.create_all(new_engine)
    return new_engine

engine = get_engine()

def get_session() -> Session:
    return Session(engine)


def create_and_add(
        sess: Session,
        model: Type[SQLModel],
        data: Dict[str, Any],
        commit: bool = True
) -> SQLModel:
    """
    Instantiate and persist a SQLModel from a dict of values.
    Filters out keys the model doesn't accept.
    """
    valid_keys = set(model.model_fields.keys())
    filtered = {k: v for k, v in data.items() if k in valid_keys}
    instance = model(**filtered)
    sess.add(instance)
    if commit:
        sess.commit()
        sess.refresh(instance)
    return instance


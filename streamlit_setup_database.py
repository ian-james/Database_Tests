import streamlit as st
from sqlmodel import SQLModel, create_engine, Session, select

@st.cache_resource
def get_engine():
    url = st.secrets["database"]["url"]
    engine = create_engine(
        url,
        connect_args={"check_same_thread": False},
        echo=False,
    )
    # runs only once per session
    SQLModel.metadata.create_all(engine)
    return engine

engine = get_engine()

def get_session() -> Session:
    return Session(engine)

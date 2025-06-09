import streamlit as st
from sqlmodel import SQLModel, create_engine, Session, select
from models import Person, Task, Project
from streamlit_setup_database import get_session

# — View Data —
def show_all_data():
    if st.checkbox("Show all Data"):
        with get_session() as sess:
            ppl = sess.exec(select(Person)).all()
            tasks = sess.exec(select(Task)).all()
            projects = sess.exec(select(Project)).all()
        st.write("People:", ppl)
        st.write("Tasks:", tasks)
        st.write("Projects:", projects)
import streamlit as st
from sqlmodel import SQLModel, create_engine, Session, select
from models import Person, Task, Project
from streamlit_setup_database import get_session
from streamlit_person_view import load_people_data
from streamlit_task_view import load_tasks_data
from streamlit_project_view import load_projects_data


# — View Data —
def show_all_data():
    if st.checkbox("Show all People"):
        ppl = load_people_data()
        st.write("People:", ppl)

    if st.checkbox("Show all Tasks"):
        tasks = load_tasks_data()
        st.write("Tasks:", tasks)

    if st.checkbox("Show all Projects"):
        projects = load_projects_data()
        st.write("Projects:", projects)

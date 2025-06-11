import streamlit as st
from sqlmodel import SQLModel, create_engine, Session, select

from models import Task
from streamlit_setup_database import get_session
from generic_form_from_sqlmodel import create_and_add, generate_form

# @st.cache_resource
# def load_tasks_data():
#     with get_session() as sess:
#         tasks = sess.exec(select(Task)).all()
#     # Convert models to plain dicts
#     return [task.model_dump(exclude_none=True) for task in tasks]

@st.cache_resource
def load_tasks_data():
    with get_session() as sess:
       return list(sess.exec(select(Task)).all())

def display_task_list():
    tasks = load_tasks_data()

    if not tasks:
        st.info("No tasks found.")
        return

    for task in tasks:
        st.subheader(task.title)
        # If the task has a person assigned display it otherwise how unassigned.
        st.write(f"Time on task: {task.time_on_task} hrs")
        st.write(f"Completed: {'Yes' if task.completed else 'No'}")
        st.markdown("---")

def display_task_form(people):
    with get_session() as session:
        form_data = generate_form(Task)
        if form_data:
            task = create_and_add(session, Task, form_data)
            st.success(f"Created task: {task.id} {task.title}")
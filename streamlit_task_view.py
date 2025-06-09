import streamlit as st
from sqlmodel import SQLModel, create_engine, Session, select
from models import Person, Task
from streamlit_setup_database import get_session
from streamlit_person_view import load_people_data


def display_task_list():
    with get_session() as sess:
        tasks = sess.exec(select(Task)).all()

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
    with st.form("task_form"):
        t_title       = st.text_input("Title")
        t_description = st.text_area("Description")
        t_time        = st.number_input("Time on task (hrs)", min_value=0.0, step=0.25)
        t_completed   = st.checkbox("Completed", value=False)
        t_person      = st.selectbox(
            "Assign to",
            options=people,
            format_func=lambda d: d["name"]
        )

        if st.form_submit_button("Add Task"):
            try:
                with get_session() as sess:
                    sess.add(Task(
                        title=t_title,
                        description=t_description,
                        time_on_task=t_time or None,
                        completed=t_completed,
                        person_id=t_person["id"]
                    ))
                    sess.commit()
                st.success(f"✅ Task “{t_title}” added to {t_person['name']}")
                load_people_data.clear()  # invalidate cache if needed elsewhere
            except Exception as e:
                st.error("❌ Could not add task.")
                st.exception(e)
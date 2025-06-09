import streamlit as st
from sqlmodel import Session, select
from typing import List

from setup_database import create_db_and_tables
from models import Person, Task, Project

# ─── Engine & Session ─────────────────────────
engine = create_db_and_tables("my_app.db")
def get_session(): return Session(engine)

# ─── Caching helpers ───────────────────────────
@st.cache_data(ttl=300)
def load_people() -> List[Person]:
    with get_session() as sess:
        return sess.exec(select(Person)).all()

@st.cache_data(ttl=300)
def load_projects() -> List[Project]:
    with get_session() as sess:
        return sess.exec(select(Project)).all()


# ─── App Layout ────────────────────────────────
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Add Person", "Add Project", "Add Task", "View Data"])

# ─── Add Person ────────────────────────────────
if page == "Add Person":
    st.title("➕ Add a New Person")
    with st.form("person_form"):
        name   = st.text_input("Name")
        age    = st.number_input("Age", min_value=0, max_value=120, step=1)
        height = st.number_input("Height (m)", min_value=0.0, step=0.01)
        if st.form_submit_button("Add Person"):
            with get_session() as sess:
                sess.add(Person(name=name, age=age, height=height))
                sess.commit()
            st.success(f"Added person: {name}")
            load_people.clear()

# ─── Add Project ───────────────────────────────
elif page == "Add Project":
    st.title("🗂️ Add a New Project")
    with st.form("project_form"):
        pname       = st.text_input("Project name")
        pdesc       = st.text_area("Description")
        pstart      = st.date_input("Start date", value=None)
        pend        = st.date_input("End date", value=None)
        if st.form_submit_button("Add Project"):
            with get_session() as sess:
                sess.add(Project(
                    name=pname,
                    description=pdesc or None,
                    start_date=pstart,
                    end_date=pend
                ))
                sess.commit()
            st.success(f"Added project: {pname}")
            load_projects.clear()

# ─── Add Task ──────────────────────────────────
elif page == "Add Task":
    st.title("📝 Add a New Task")

    people   = load_people()
    projects = load_projects()

    if not people:
        st.warning("Add at least one Person first.")
    elif not projects:
        st.warning("Add at least one Project first.")
    else:
        with st.form("task_form"):
            t_title = st.text_input("Title")
            t_description = st.text_area("Description")
            t_time  = st.number_input("Time on task (hrs)", min_value=0.0, step=0.25)
            t_person = st.selectbox("Assign to Person", people, format_func=lambda p: p.name)
            t_project= st.selectbox("Belongs to Project", projects, format_func=lambda pr: pr.name)
            t_completed = st.checkbox("Completed", value=False)

            if st.form_submit_button("Add Task"):
                with get_session() as sess:
                    sess.add(Task(
                        title=t_title,
                        description=t_description or None,
                        time_on_task=t_time or None,
                        completed=t_completed,
                        person_id=t_person.id,
                        project_id=t_project.id
                    ))
                    sess.commit()
                st.success(f"Task “{t_title}” added to {t_project.name}")
                # no need to clear caches here unless you reuse them elsewhere

# ─── View Data ──────────────────────────────────
elif page == "View Data":
    st.title("📋 View Current Data")
    with get_session() as sess:
        ppl = sess.exec(select(Person)).all()
        prj = sess.exec(select(Project)).all()
        tks = sess.exec(select(Task)).all()

    st.subheader("Projects")
    if prj:
        st.table([{"ID": p.id, "Name": p.name, "Start": p.start_date, "End": p.end_date} for p in prj])
    else:
        st.info("No projects yet.")

    st.subheader("Tasks")
    if tks:
        st.table([{
            "ID": t.id,
            "Title": t.title,
            "Person": next((x.name for x in ppl if x.id==t.person_id), "--"),
            "Project": next((x.name for x in prj if x.id==t.project_id), "--"),
            "Completed": t.completed,
            "Time (hrs)": t.time_on_task
        } for t in tks])
    else:
        st.info("No tasks yet.")

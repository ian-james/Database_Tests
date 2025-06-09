import streamlit as st
from sqlmodel import select
from streamlit_setup_database import get_session
from models import Project

# ─── 1. Cached “pure data” version of projects ─────────
@st.cache_data(ttl=300)
def load_projects_data():
    with get_session() as sess:
        rows = sess.exec(select(Project)).all()
    # Turn models into plain dicts
    return [{"id": p.id, "name": p.name} for p in rows]

# ─── Streamlit UI ───────────────────────────────────
def display_projects():
    st.title("Project Manager")
    projects = load_projects_data()

    if not projects:
        st.info("Add at least one project first.")
    else:
        st.subheader("Projects")
        for project in projects:
            # Add a card to display each project
            with st.expander(project["name"], expanded=False):
                st.write(f"ID: {project['id']}")
                st.button("View", key=project["id"], on_click=display_project, args=(project["id"],))

    add_project_form()

def display_project( project_id):
    projects = load_projects_data()
    project = next((p for p in projects if p["id"] == project_id), None)

    if project:
        st.subheader(f"Project: {project['name']}")
        st.write(f"ID: {project['id']}")
        st.write(f"Description: {project.get('description', 'No description provided')}")
    else:
        st.error("Project not found.")

def add_project_form():
    with st.form("project_form"):
        name = st.text_input("Project Name")
        description = st.text_area("Description")
        if st.form_submit_button("Add Project"):
            with get_session() as sess:
                sess.add(Project(name=name,
                                 description=description))
                sess.commit()
            st.success(f"Added: {name}")
            # Clear cache so new project shows up in Project dropdown
            load_projects_data.clear()
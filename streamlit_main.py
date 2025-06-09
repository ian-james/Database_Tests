import streamlit as st
from sqlmodel import SQLModel, create_engine, Session, select
from models import Person, Task
from streamlit_setup_database import get_session

from streamlit_person_view import load_people_data, display_people, display_add_person_form
from streamlit_task_view import display_task_form, display_task_list
from streamlit_show_all_info import show_all_data
from streamlit_project_view import display_project, display_projects

def main():
    st.title("Task Management App")
    st.sidebar.title("Navigation")

    # Navigation options
    page = st.sidebar.radio("Go to", ["People", "Tasks", "Projects", "Show All Data"])

    if page == "People":
        display_people()
        display_add_person_form()
    elif page == "Tasks":
        people = load_people_data()
        display_task_list()
        display_task_form(people)
    elif page == "Projects":
        display_projects()
    elif page == "Show All Data":
        show_all_data()

if __name__ == "__main__":
    main()
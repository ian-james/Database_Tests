import streamlit as st

from streamlit_person_view import load_people_data, display_people, display_add_person_form, display_person_tasks, \
    assign_task_to_person, select_a_task_from_unassigned_tasks
from streamlit_task_view import display_task_form, display_task_list
from streamlit_show_all_info import show_all_data
from streamlit_project_view import display_projects, add_project_form
from streamlit_generic_form import generate_form
from models import Tag

# TODO:
# People aren't adding anymore
# Tag doesn't show at all because Priority already defined.
# View Tasks  = load_tasks_data()


def setup_people_page():
    st.title("People Management")
    if st.sidebar.button("Add Person"):
        display_add_person_form()
    elif st.sidebar.button("View People"):
        display_people()
    elif st.sidebar.button("View Person Tasks"):
        person_id = st.sidebar.selectbox("Select a Person", options=load_people_data(), format_func=lambda d: d.name)
        display_person_tasks(person_id)
    elif st.sidebar.button("Assign Task to Person"):
        task_id = select_a_task_from_unassigned_tasks()
        if task_id:
            person_id = st.sidebar.selectbox("Select a Person to assign", options=load_people_data(),
                                             format_func=lambda d: d.name)
            assign_task_to_person(task_id, person_id)


def main():
    # Navigation options
    page = st.sidebar.radio("Go to", ["People", "Tag", "Tasks", "Projects", "Show All Data"])

    st.title("Task Management App")
    st.sidebar.title("Navigation")


    if page == "People":
        setup_people_page()
    elif page == "Tasks":
        setup_task_page()
    elif page == "Projects":
        setup_projects_page()
    elif page == "Tag":
        generate_form(Tag)
    elif page == "Show All Data":
        show_all_data()


def setup_projects_page():
    if st.sidebar.button("Add Project"):
        add_project_form()
    elif st.sidebar.button("View Projects"):
        display_projects()


def setup_task_page():
    if st.sidebar.button("Add Task"):
        people = load_people_data()
        display_task_form(people)
    elif st.sidebar.button("View Tasks"):
        display_task_list()
    elif st.sidebar.button("Assign Task to Person"):
        task_id = select_a_task_from_unassigned_tasks()
        if task_id:
            person_id = st.sidebar.selectbox("Select a Person to assign", options=load_people_data(),
                                             format_func=lambda d: d.name)
            assign_task_to_person(task_id, person_id)


if __name__ == "__main__":
    main()

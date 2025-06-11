import streamlit as st
from sqlmodel import select
from setup_database import get_session
from models import Person, Task

# ─── 2. Cached “pure data” version of people ─────────
@st.cache_data(ttl=300)
def load_people_data( ) -> list[Person]:
    with get_session() as sess:
        return list(sess.exec(select(Person)).all())


@st.cache_data(ttl=300)
def load_person_tasks_data(person_id: int) -> list[Task]:
    with get_session() as sess:
        return list(sess.exec(
            select(Task).where(Task.person_id == person_id).scalars()
        ).all())

# Load tasks where no one is assigned
@st.cache_data(ttl=300)
def load_unassigned_tasks_data() -> list[Task]:
    with get_session() as sess:
        return list(sess.exec(
            select(Task).where(Task.person_id.is_(None)).scalars()
        ).all())

    # Turn models into plain dicts
    # if include_tasks:
    #     return [p.model_dump(exclude_none=True) for p in people]
    # return [p.model_dump(exclude_none=True, exclude={"tasks"}) for p in people]


# ─── Streamlit UI ───────────────────────────────────
def display_people():
    people = load_people_data()

    if not people:
        st.info("Add at least one person first.")
    else:
        st.subheader("People")
        for person in people:
            st.write(f"{person.name} (ID: {person.id})")
            st.write(f"{person.age} years old, {person.height} tall")

def display_add_person_form():
    with st.form("person_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        height = st.number_input("Height (m)", min_value=0.0, step=0.01)
        if st.form_submit_button("Add Person"):
            with get_session() as sess:
                sess.add(Person(name=name, age=age, height=height))
                sess.commit()
            st.success(f"Added: {name}")
            # Clear cache so new person shows up in Task dropdown
            load_people_data.clear()

def display_person_tasks(person_id):

    tasks = load_person_tasks_data(person_id)

    if not tasks:
        st.info("No tasks assigned to this person.")
        return

    st.subheader(f"Tasks for {person_id}")
    for task in tasks:
        st.write(f"Title: {task.title}")
        st.write(f"Description: {task.description or 'No description'}")
        st.write(f"Time on task: {task.time_on_task} hrs")
        st.write(f"Completed: {'Yes' if task.completed else 'No'}")
        st.markdown("---")
def assign_task_to_person(task_id, person_id):
    with get_session() as sess:
        task = sess.get(Task, task_id)
        if task:
            task.person_id = person_id
            sess.commit()
            st.success(f"Task {task.title} assigned to person ID {person_id}")
        else:
            st.error("Task not found.")

def select_a_task_from_unassigned_tasks():
    with get_session() as sess:
        tasks = sess.exec(select(Task).where(Task.person_id.is_(None))).all()

    if not tasks:
        st.info("No unassigned tasks available.")
        return None

    task_options = {task.id: task.title for task in tasks}
    selected_task_id = st.selectbox("Select a task to assign", options=list(task_options.keys()), format_func=lambda x: task_options[x])

    return selected_task_id
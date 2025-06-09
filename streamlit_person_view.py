import streamlit as st
from sqlmodel import select
from streamlit_setup_database import get_session
from models import Person, Task


# ─── 2. Cached “pure data” version of people ─────────
@st.cache_data(ttl=300)
def load_people_data():
    with get_session() as sess:
        rows = sess.exec(select(Person)).all()
    # Turn models into plain dicts
    return [{"id": p.id, "name": p.name} for p in rows]


# ─── Streamlit UI ───────────────────────────────────
def display_people():
    st.title("Task & Person Manager")
    people = load_people_data()

    if not people:
        st.info("Add at least one person first.")
    else:
        st.subheader("People")
        for person in people:
            st.write(f"{person['name']} (ID: {person['id']})")

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

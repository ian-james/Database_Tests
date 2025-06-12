import solara
from typing import Type
from sqlmodel import SQLModel

from Solara_ModelForm import ModelForm
from Solara_Table import ModelTable
from setup_database import get_session, create_and_add

from models import Person

@solara.component()
def Page():
    status, set_status = solara.use_state("")

    def add_person(model: Type[SQLModel], payload):
        with get_session() as session:
            person = create_and_add(session, model, payload)
            set_status(f"Created Person: {person.id} {person.name}")

    ModelForm(model=Person, fields=["name", "age", "height"], defaults={"age": 18, "height": 1.75},
              on_submit=add_person)

    if status:
        solara.Success(status)

    solara.Markdown("## People List")
    ModelTable(Person, items_per_page=10)

def main():
    Page()

if __name__ == "__main__":
    main()

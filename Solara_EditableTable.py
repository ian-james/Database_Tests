import solara
from typing import Type, Sequence, Any
from sqlmodel import SQLModel, select

from Solara_ModelForm import ModelForm
from setup_database import get_session
from solara_load_data import load_all_database_items


@solara.component
def EditableSQLModelTable(
    *,
    model: Type[SQLModel],
    fields: Sequence[str],
):
    # state to hold list of items + which one’s being edited
    items, set_items = solara.use_state([])
    editing_id, set_editing_id = solara.use_state(None)

    def load_items():
        rows = load_all_database_items(model)
        set_items(rows)

    def delete_item(item_id: int):
        with get_session() as sess:
            obj = sess.exec( select(model).where(model.id == item_id)).one_or_none()
            if obj:
                sess.delete(obj)
                sess.commit()
        load_items()

    def update_item(model: Type[SQLModel], data: dict[str, Any]):
        # assumes data["id"] present
        with get_session() as sess:
            obj = sess.get(model, data["id"])
            for k, v in data.items():
                setattr(obj, k, v)
            sess.add(obj)
            sess.commit()
        set_editing_id(None)
        load_items()

    # initial load
    solara.use_effect(load_items, [])

    with solara.VBox():
        for row in items:
            row_id = getattr(row, "id", None)
            with solara.HBox():
                # show a summary of the row
                solara.Markdown(f"`{row.__class__.__name__}` {row_id}: \“{row.dict()}\”")
                solara.Button("Edit", on_click=lambda rid=row_id: set_editing_id(rid))
                solara.Button("Delete", on_click=lambda rid=row_id: delete_item(rid))

            # if this row is in edit mode, show the form
            if editing_id == row_id:
                defaults = row.dict()
                # ensure the form has the primary key so update_item can find it
                ModelForm(
                    model=model,
                    fields=["id", *fields],
                    defaults=defaults,
                    on_submit=update_item,
                )
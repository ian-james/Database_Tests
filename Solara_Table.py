import solara
import pandas as pd
from typing import Type
from sqlmodel import SQLModel
from solara_load_data import load_all_database_items

@solara.component
def ModelTable( model: Type[SQLModel], items_per_page: int = 10):

    items = load_all_database_items(model)

    if not items:
        solara.Text(f"No {model.__name__} items found.")
        return

    df = pd.DataFrame([item.dict() for item in items])
    solara.DataFrame(df, items_per_page=items_per_page)

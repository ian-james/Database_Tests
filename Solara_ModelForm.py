import solara
from typing import Sequence, Any, Callable, Type
from sqlmodel import SQLModel
from render_ui_fields import renderInputType

@solara.component
def ModelForm( *,
               model:Type[SQLModel],
    fields: Sequence[str],
    defaults: dict[str, Any] | None = None,
    on_submit: Callable[[Type[SQLModel],
                         dict[str, Any]],
    None]):

    # Initialize a state based on
    state = {}
    for f in fields:
        init = defaults[f] if defaults and f in defaults else ""
        state[f] = solara.use_state(init)

    with solara.Card(f"Add/Edit {model.__name__}"):
        for f in fields:
            value, set_value = state[f]
            renderInputType(f.capitalize(), value, set_value)

        solara.Button(label="Submit",
            on_click=lambda: on_submit(model, {field: state[field][0] for field in fields})
        )
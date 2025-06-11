import solara
from typing import Sequence, Any, Callable, Type

from sqlmodel import SQLModel


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

            if isinstance(value, bool):
                solara.Checkbox(label=f.capitalize(), value=value, on_value=set_value)
            elif isinstance(value, float):
                solara.InputFloat(label=f.capitalize(), value=value, on_value=set_value)
            elif isinstance(value, int):
                solara.InputInt(label=f.capitalize(), value=value, on_value=set_value)

            else:
                solara.InputText(label=f.capitalize(), value=value, on_value=set_value)

        if solara.Button("Submit"):
            payload = {f: state[f][0] for f in fields}
            on_submit(model,payload)
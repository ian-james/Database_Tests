import solara
from typing import Any, Callable


def renderInputType(label: str, value: Any, on_value: Callable[[Any], None]):
    if isinstance(value, bool):
        solara.Checkbox(label=label, value=value, on_value=on_value)
    elif isinstance(value, float):
        solara.InputFloat(label=label, value=value, on_value=on_value)
    elif isinstance(value, int):
        solara.InputInt(label=label, value=value, on_value=on_value)
    else:
        solara.InputText(label=label, value=value, on_value=on_value)

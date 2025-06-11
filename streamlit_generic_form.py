import streamlit as st
from typing import Type, Any, Dict
from datetime import date, datetime
from enum import Enum
import inspect
from sqlmodel import SQLModel, Session

# --- Field Introspection Helpers ---
def get_field_meta(field: Any) -> Dict[str, Any]:
    name = getattr(field, 'name', None)
    default = getattr(field, 'default', None)
    outer_type = getattr(field, 'outer_type_', None)
    read_only = getattr(field, 'field_info', {}).extra.get('read_only', False) if hasattr(field, 'field_info') else False
    return {'name': name, 'type': outer_type, 'default': default, 'read_only': read_only}

# --- Input Renderers ---
def render_input(label: str, python_type: Any, default: Any) -> Any:
    if inspect.isclass(python_type) and issubclass(python_type, Enum):
        options = list(python_type)
        default_idx = options.index(default) if default in options else 0
        return st.selectbox(label, options, index=default_idx)
    if python_type is str:
        return st.text_input(label, default or "")
    if python_type is int:
        return st.number_input(label, value=default or 0, step=1)
    if python_type is float:
        return st.number_input(label, value=default or 0.0)
    if python_type is bool:
        return st.checkbox(label, value=bool(default))
    if python_type in (date, datetime):
        return st.date_input(label, value=default or date.today())
    return None

# --- Form Generator ---
def generate_form(model: Type[SQLModel]) -> Dict[str, Any]:
    st.header(f"Create a new {model.__name__}")
    form_values: Dict[str, Any] = {}
    with st.form(key=model.__name__):
        for field in getattr(model, '__fields__', {}).values():
            meta = get_field_meta(field)
            if meta['read_only'] or meta['type'] is None:
                continue
            label = meta['name'].replace('_', ' ').title()
            value = render_input(label, meta['type'], meta['default'])
            if value is not None:
                form_values[meta['name']] = value
        submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Form submitted successfully!")
        st.json(form_values)
        return form_values
    return {}
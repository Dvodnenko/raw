from datetime import datetime

from ..domain import InvalidValue
from ..shared import MISSING, _Missing
from .constants import EDITOR_SENTINEL
from .editor import from_editor


def resolve_arg(name: str, value: str | _Missing, initial_text: str = "") -> str | None | _Missing:
    """
    resolves the tri-state UX logic. does NOT parse/cast data types
    """
    if value is MISSING:
        return MISSING
    if value == EDITOR_SENTINEL:
        value = from_editor(name, initial_text)
    if value.lower() == "null":
        return None
    return value


def parse_datetime(value: str | None, name: str):
    if value in (None, MISSING):
        return value

    try:    
        dt = datetime.fromisoformat(value)
    except ValueError:
        raise InvalidValue(f"invalid {name} format")
    return dt.replace(microsecond=0)

import dateparser

from ..domain import InvalidValue
from ..shared import MISSING, _Missing
from .constants import EDITOR_SENTINEL
from .editor import from_editor


def resolve_arg(name: str, value: str | _Missing) -> str | None:
    """
    resolves the tri-state UX logic. does NOT parse/cast data types
    """
    if value is MISSING:
        return None
    if value == EDITOR_SENTINEL:
        return from_editor(name)
    return value


def parse_datetime(value: str | None, name: str):
    if value is None:
        return None
    
    dt = dateparser.parse(value)
    if not dt: # dateparser couldn't parse it => invalid format
        raise InvalidValue(f"invalid {name} format")
    return dt

def parse_enum[T](value: str | None, enum: type[T], name: str) -> T | None:
    if value is None:
        return None
    try:
        return enum(value.lower())
    except (ValueError, KeyError) as exc:
        raise InvalidValue(f"invalid {name}") from exc

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

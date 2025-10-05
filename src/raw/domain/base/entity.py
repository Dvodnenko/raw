from dataclasses import dataclass, field
from typing import Optional

from .enums import Color


@dataclass(eq=False)
class Entity:

    title: str
    parent: Optional["Entity"] = None
    refs: list["Entity"]
    color: Color = field(default=Color.WHITE, kw_only=True)
    icon: str | None = field(default=None, kw_only=True)

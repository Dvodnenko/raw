from dataclasses import dataclass, field

from .enums import Color


@dataclass(eq=False)
class Entity:

    id: int
    parent: int
    title: str
    refs: list[int]
    color: Color = field(default=Color.WHITE, kw_only=True)
    icon: str | None = field(default=None, kw_only=True)

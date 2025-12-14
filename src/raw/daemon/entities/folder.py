from dataclasses import dataclass, field

from .entity import Entity


@dataclass(kw_only=True, eq=False)
class Folder(Entity):
    children: list["Entity"] = field(
        default_factory=lambda: [])

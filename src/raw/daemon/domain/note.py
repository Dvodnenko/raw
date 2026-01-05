from dataclasses import dataclass

from .entity import Entity


@dataclass(kw_only=True, eq=False)
class Note(Entity):
    
    content: str = ""

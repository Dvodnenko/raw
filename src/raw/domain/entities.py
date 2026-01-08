from dataclasses import dataclass, field
from datetime import datetime

from .value_objects import Styles


def now():
    return datetime.now().replace(microsecond=0)


@dataclass(kw_only=True)
class Entity:
    id: int
    title: str
    description: str = ""
    styles: Styles = Styles()
    icon: str = ""
    links: list[int] = field(default_factory=list)

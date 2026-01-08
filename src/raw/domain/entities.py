from dataclasses import dataclass, field
from datetime import datetime

from .value_objects import Styles
from .enums import TaskStatus


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


@dataclass(kw_only=True)
class Task(Entity):
    
    status: TaskStatus = TaskStatus.ACTIVE
    deadline: datetime = None

    def mark(self, value: str):
        try:
            self.status = TaskStatus(value)
        except ValueError:
            raise ValueError(f"No such status: {value}") from None

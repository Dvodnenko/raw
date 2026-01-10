from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .enums import TaskStatus


def now() -> datetime:
    return datetime.now().replace(microsecond=0)


@dataclass(kw_only=True)
class Entity:
    id: int
    title: str
    description: str = ""
    icon: str = ""
    parent_id: Optional[int] = None

    def __post_init__(self):
        if self.title == "" or self.title.strip() == "":
            raise ValueError("Title cannot be empty")


@dataclass(kw_only=True)
class Task(Entity):
    
    status: TaskStatus = TaskStatus.ACTIVE
    deadline: Optional[datetime] = None

    def mark(self, value: str):
        try:
            self.status = TaskStatus(value)
        except ValueError:
            raise ValueError(f"No such status: {value}") from None

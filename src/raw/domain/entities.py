from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re

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

    _title_pattern = re.compile(r"^/(?:[A-Za-z0-9 _-]+)(?:/[A-Za-z0-9 _-]+)*$")

    def __post_init__(self):
        if not self._title_pattern.match(self.title):
            raise ValueError(f"The title doesn't match the pattern: {self._title_pattern.pattern}")


@dataclass(kw_only=True)
class Task(Entity):
    
    status: TaskStatus = TaskStatus.ACTIVE
    deadline: Optional[datetime] = None

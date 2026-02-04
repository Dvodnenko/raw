from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re

from .enums import TaskStatus
from .exc import InvalidValue, InvalidState


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
        if not self.title or self.title.strip == "":
            raise InvalidValue("title cannot be empty")
        if not self._title_pattern.match(self.title):
            raise InvalidValue("title is invalid")


@dataclass(kw_only=True)
class Task(Entity):
    
    status: TaskStatus = TaskStatus.INACTIVE
    deadline: Optional[datetime] = None

@dataclass(kw_only=True)
class Note(Entity):
    content: str = ""

@dataclass(kw_only=True)
class Session(Entity):
    message: str = ""
    summary: str = ""
    started_at: datetime
    ended_at: Optional[datetime] = None

    def __post_init__(self):
        super().__post_init__()
        if self.started_at is None:
            raise InvalidValue("start time is required")
        if not self.is_active:
            if self.started_at > self.ended_at:
                raise InvalidState("start time cannot be later than end time")

    @property
    def is_active(self):
        return self.ended_at is None

    @property
    def duration(self):
        return (self.ended_at or now()) - self.started_at

@dataclass(kw_only=True)
class Folder(Entity):
    ...

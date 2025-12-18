from dataclasses import dataclass
from datetime import datetime

from .entity import Entity
from .enums import TaskStatus


@dataclass(kw_only=True, eq=False)
class Task(Entity):

    deadline: datetime = None
    status: TaskStatus = TaskStatus.INACTIVE

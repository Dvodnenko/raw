from dataclasses import dataclass
from datetime import datetime

from .entity import Entity
from .enums import TaskStatus


@dataclass(kw_only=True, eq=False)
class Task(Entity):

    deadline: datetime = None
    status: TaskStatus = TaskStatus.INACTIVE

    def to_dict(self):
        return {
            ## From Entity
            **super().to_dict(),

            # Task's itself
            "deadline": self.deadline,
            "status": self.status.name,
        }

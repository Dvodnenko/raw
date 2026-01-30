from typing import Optional
from datetime import datetime

from .entities import Task
from .enums import TaskStatus
from ..shared import MISSING


class TaskEditor:
    def __init__(
        self,
        title: Optional[str] = MISSING,
        description: Optional[str] = MISSING,
        icon: Optional[str] = MISSING,
        status: Optional[TaskStatus] = MISSING,
        deadline: Optional[datetime] = MISSING,
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.status = status
        self.deadline = deadline

    def apply(self, task: Task) -> Task:
        return Task(
            id=task.id,
            title=self.title if self.title is not MISSING else task.title,
            description=(
                self.description
                if self.description is not MISSING
                else task.description
            ),
            icon=self.icon if self.icon is not MISSING else task.icon,
            parent_id=task.parent_id, # it cannot be changed here
            status=self.status if self.status is not MISSING else task.status,
            deadline=self.deadline if self.deadline is not MISSING else task.deadline,
        )

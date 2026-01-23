from typing import Optional
from datetime import datetime

from .entities import Task
from .enums import TaskStatus


_sentinel = object()


class TaskEditor:
    def __init__(
        self,
        title: Optional[str] = _sentinel,
        description: Optional[str] = _sentinel,
        icon: Optional[str] = _sentinel,
        status: Optional[TaskStatus] = _sentinel,
        deadline: Optional[datetime] = _sentinel,
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.status = status
        self.deadline = deadline

    def apply(self, task: Task) -> Task:
        return Task(
            id=task.id,
            title=self.title if self.title is not _sentinel else task.title,
            description=(
                self.description
                if self.description is not _sentinel
                else task.description
            ),
            icon=self.icon if self.icon is not _sentinel else task.icon,
            status=self.status if self.status is not _sentinel else task.status,
            deadline=self.deadline if self.deadline is not _sentinel else task.deadline,
        )

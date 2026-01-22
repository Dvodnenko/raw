from dataclasses import dataclass
from typing import Optional, Iterator
from datetime import datetime

from ...domain import UnitOfWork, Spec, TaskStatus


@dataclass(frozen=True)
class FindTaskQuery:
    spec: Spec

@dataclass(frozen=True)
class TaskView:
    id: int
    title: str
    description: str
    icon: str
    parent_id: Optional[int]
    status: TaskStatus
    deadline: Optional[datetime]


class FindTask:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find(self, query: FindTaskQuery) -> Iterator[TaskView]:
        with self.uow:
            for task in self.uow.tasks.filter(query.spec):
                yield TaskView(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    icon=task.icon,
                    parent_id=task.parent_id,
                    status=task.status,
                    deadline=task.deadline,
                )

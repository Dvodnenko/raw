from dataclasses import dataclass
from typing import Optional, Iterator
from datetime import datetime

from ...domain import UnitOfWork, Spec, TaskStatus, InvalidValue


@dataclass(frozen=True)
class TaskView:
    id: int
    title: str
    description: str
    icon: str
    parent_id: Optional[int]
    status: TaskStatus
    deadline: Optional[datetime]

@dataclass(frozen=True)
class FindTaskQuery:
    spec: Spec
    
    # Optionals
    order_by: str
    reverse: bool = False

class FindTask:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find(self, query: FindTaskQuery) -> Iterator[TaskView]:
        with self.uow:
            for task in self.uow.tasks.filter(
                query.spec,
                query.order_by,
                query.reverse,
            ):
                yield TaskView(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    icon=task.icon,
                    parent_id=task.parent_id,
                    status=task.status,
                    deadline=task.deadline,
                )


@dataclass(frozen=True)
class FindEntityQuery:
    type: str
    spec: Spec

    # Optionals
    order_by: str
    reverse: bool = False

class FindEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find(self, cmd: FindEntityQuery):
        if cmd.type == "task":
            yield from (
                FindTask(self.uow)
                .find(
                    FindTaskQuery(
                        cmd.spec, cmd.order_by, cmd.reverse
                    )
                )
            )
            return
        else:
            raise InvalidValue("unknown entity type")

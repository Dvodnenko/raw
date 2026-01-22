from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ...domain import Task, TaskStatus, UnitOfWork
from ..common import _extract_parent_title


@dataclass(frozen=True)
class AddTaskCmd:
    title: str
    description: str = ""
    icon: str = ""
    status: TaskStatus = TaskStatus.ACTIVE
    deadline: datetime = None

class AddTask:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add(self, cmd: AddTaskCmd):
        obj = Task(
            # repository will generate the id by itself 
            # and we don't really need it here
            id=None,
            title=cmd.title,
            description=cmd.description,
            icon=cmd.icon,
            status=cmd.status,
            deadline=cmd.deadline,
        )

        parent_path: Optional[str] = _extract_parent_title(cmd.title)

        with self.uow:
            if parent_path:
                parent = self.uow.tasks.get_by_title(parent_path)
                if not parent:
                    raise ValueError(
                        f"Cannot locate Task in {parent_path}/ because it does not exist"
                    )
                obj.parent_id = parent.id

            self.uow.tasks.add(obj)

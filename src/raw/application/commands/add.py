from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

from ...domain import (
    Task, TaskStatus, UnitOfWork,
    NotFound, AlreadyExists, InvalidValue, EntityRef
)
from ..common import _extract_parent_title


@dataclass(frozen=True)
class AddTaskCmd:
    title: Optional[str] = ""
    description: Optional[str] = ""
    icon: Optional[str] = ""
    status: Optional[TaskStatus] = TaskStatus.ACTIVE
    deadline: Optional[datetime] = None

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
            exists = self.uow.tasks.get_by_title(obj.title) is not None
            if exists:
                raise AlreadyExists(EntityRef(obj.title))

            if parent_path:
                parent = self.uow.tasks.get_by_title(parent_path)
                if not parent:
                    raise NotFound(EntityRef(parent_path))
                obj.parent_id = parent.id

            self.uow.tasks.add(obj)


@dataclass(frozen=True)
class AddEntityCmd:
    type: str
    fields: dict[str, Any]

class AddEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add(self, cmd: AddEntityCmd):
        if cmd.type == "task":
            AddTask(self.uow).add(AddTaskCmd(**cmd.fields))
        else:
            raise InvalidValue("unknown entity type")

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ....domain import (
    Task, UnitOfWork,
    NotFound, AlreadyExists, EntityRef
)
from ...common import _extract_parent_title


@dataclass(frozen=True)
class AddTaskCmd:
    title: Optional[str] = ""
    description: Optional[str] = ""
    icon: Optional[str] = ""
    status: Optional[str] = ""
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
            already_exists = self.uow.intertype.resolve_type_by_title(obj.title) is not None
            if already_exists:
                raise AlreadyExists(EntityRef(obj.title))

            if parent_path:
                parent_id = self.uow.intertype.resolve_id_by_title(parent_path)
                if not parent_id:
                    raise NotFound(EntityRef(parent_path))
                obj.parent_id = parent_id

            self.uow.tasks.add(obj)

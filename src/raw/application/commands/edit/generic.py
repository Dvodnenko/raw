from dataclasses import dataclass
from typing import Any

from ....domain import UnitOfWork, TaskEditor, NotFound, EntityRef, EntityType
from .task import EditTask, EditTaskCmd


@dataclass(frozen=True)
class EditEntityCmd:
    id: int
    fields: dict[str, Any]

class EditEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def edit(self, cmd: EditEntityCmd):
        with self.uow:
            type = self.uow.intertype.resolve_type(cmd.id)

        if not type:
            raise NotFound(EntityRef(cmd.id))
        
        if type is EntityType.TASK:
            cmd = EditTaskCmd(
                cmd.id,
                TaskEditor(**cmd.fields)
            )
            EditTask(self.uow).edit(cmd)

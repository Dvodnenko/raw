from dataclasses import dataclass
from typing import Any

from ....domain import UnitOfWork, TaskEditor, NotFound, EntityRef, EntityType
from ...identifier import Identifier
from .task import EditTask, EditTaskCmd


@dataclass(frozen=True)
class EditEntityCmd:
    identifier: Identifier
    fields: dict[str, Any]

class EditEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def edit(self, cmd: EditEntityCmd):
        with self.uow:
            if cmd.identifier.is_id:
                type = self.uow.intertype.resolve_type(int(cmd.identifier.value))
            else:
                type = self.uow.intertype.resolve_type_by_title(cmd.identifier.value)

        if not type:
            raise NotFound(EntityRef(cmd.identifier.value))
        
        if type is EntityType.TASK:
            cmd = EditTaskCmd(
                cmd.identifier,
                TaskEditor(**cmd.fields)
            )
            EditTask(self.uow).edit(cmd)

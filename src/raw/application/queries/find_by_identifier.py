from dataclasses import dataclass

from ...domain import UnitOfWork, EntityType, NotFound, EntityRef
from .find import TaskView, NoteView
from ..identifier import Identifier


@dataclass(frozen=True)
class FindEntityByIdentifierQuery:
    identifier: Identifier


class FindEntityByIdentifier:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find(self, cmd: FindEntityByIdentifierQuery):
        with self.uow:
            type: EntityType = None
            id: int = None

            if cmd.identifier.is_id:
                type = self.uow.intertype.resolve_type(int(cmd.identifier.value))
                id = int(cmd.identifier.value)
            else:
                type = self.uow.intertype.resolve_type_by_title(cmd.identifier.value)
                id = self.uow.intertype.resolve_id_by_title(cmd.identifier.value)

            if not type:
                raise NotFound(EntityRef(cmd.identifier.value))

            if type is EntityType.TASK:
                task = self.uow.tasks.get_by_id(id)
                
                return TaskView(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    icon=task.icon,
                    parent_id=task.parent_id,
                    status=task.status,
                    deadline=task.deadline,
                )
            elif type is EntityType.NOTE:
                note = self.uow.notes.get_by_id(id)
                
                return NoteView(
                    id=note.id,
                    title=note.title,
                    description=note.description,
                    icon=note.icon,
                    parent_id=note.parent_id,
                    content=note.content,
                )

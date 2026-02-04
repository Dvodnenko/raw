from dataclasses import dataclass

from ...domain import UnitOfWork, EntityType, NotFound, EntityRef
from .find import TaskView, NoteView, SessionView, FolderView
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

            match type:
                case EntityType.TASK:
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
                case EntityType.NOTE:
                    note = self.uow.notes.get_by_id(id)
                    
                    return NoteView(
                        id=note.id,
                        title=note.title,
                        description=note.description,
                        icon=note.icon,
                        parent_id=note.parent_id,
                        content=note.content,
                    )
                case EntityType.SESSION:
                    session = self.uow.sessions.get_by_id(id)
                    
                    return SessionView(
                        id=session.id,
                        title=session.title,
                        description=session.description,
                        icon=session.icon,
                        parent_id=session.parent_id,
                        message=session.message,
                        summary=session.summary,
                        started_at=session.started_at,
                        ended_at=session.ended_at,
                        is_active=session.is_active,
                        duration=session.duration
                    )
                case EntityType.FOLDER:
                    folder = self.uow.folders.get_by_id(id)
                        
                    return FolderView(
                        id=folder.id,
                        title=folder.title,
                        description=folder.description,
                        icon=folder.icon,
                        parent_id=folder.parent_id,
                    )

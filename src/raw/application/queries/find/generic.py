from dataclasses import dataclass

from ....domain import UnitOfWork, Spec, Task, Note, Session, Folder
from .task import TaskView
from .note import NoteView
from .session import SessionView
from .folder import FolderView


@dataclass(frozen=True)
class FindEntityQuery:
    types: tuple[str]
    spec: Spec

    # Optionals
    order_by: str
    reverse: bool = False

class FindEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find(self, cmd: FindEntityQuery):
        with self.uow:
            gen = self.uow.intertype.filter(
                types=cmd.types,
                spec=cmd.spec,
                order_by=cmd.order_by,
                reverse=cmd.reverse,
            )

            for entity in gen:
                match entity:
                    case Task() as task:
                        yield TaskView(
                            id=task.id,
                            title=task.title,
                            description=task.description,
                            icon=task.icon,
                            parent_id=task.parent_id,
                            status=task.status,
                            deadline=task.deadline,
                        )
                    case Note() as note:
                        yield NoteView(
                            id=note.id,
                            title=note.title,
                            description=note.description,
                            icon=note.icon,
                            parent_id=note.parent_id,
                            content=note.content
                        )
                    case Session() as session:
                        yield SessionView(
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
                            duration=session.duration,
                        )
                    case Folder() as folder:
                        yield FolderView(
                            id=folder.id,
                            title=folder.title,
                            description=folder.description,
                            icon=folder.icon,
                            parent_id=folder.parent_id,
                        )

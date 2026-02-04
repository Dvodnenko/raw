from dataclasses import dataclass

from ....domain import UnitOfWork, Spec, InvalidValue
from .task import FindTask, FindTaskQuery
from .note import FindNote, FindNoteQuery
from .session import FindSession, FindSessionQuery
from .folder import FindFolder, FindFolderQuery


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
        match cmd.type:
            case "task":
                yield from (FindTask(self.uow).find(FindTaskQuery(cmd.spec, cmd.order_by, cmd.reverse)))
            case "note":
                yield from (FindNote(self.uow).find(FindNoteQuery(cmd.spec, cmd.order_by, cmd.reverse)))
            case "session":
                yield from (FindSession(self.uow).find(FindSessionQuery(cmd.spec, cmd.order_by, cmd.reverse)))
            case "folder":
                yield from (FindFolder(self.uow).find(FindFolderQuery(cmd.spec, cmd.order_by, cmd.reverse)))
            case _:
                raise InvalidValue("unknown entity type")

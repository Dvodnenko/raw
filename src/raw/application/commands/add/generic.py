from dataclasses import dataclass
from typing import Any

from ....domain import UnitOfWork,InvalidValue
from .task import AddTask, AddTaskCmd
from .note import AddNote, AddNoteCmd
from .session import AddSession, AddSessionCmd


@dataclass(frozen=True)
class AddEntityCmd:
    type: str
    fields: dict[str, Any]

class AddEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add(self, cmd: AddEntityCmd):
        match cmd.type:
            case "task":
                AddTask(self.uow).add(AddTaskCmd(**cmd.fields))
            case "note":
                AddNote(self.uow).add(AddNoteCmd(**cmd.fields))
            case "session":
                AddSession(self.uow).add(AddSessionCmd(**cmd.fields))
            case _:
                raise InvalidValue("unknown entity type")

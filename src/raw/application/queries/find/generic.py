from dataclasses import dataclass

from ....domain import UnitOfWork, Spec, InvalidValue
from .task import FindTask, FindTaskQuery
from .note import FindNote, FindNoteQuery


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
        if cmd.type == "task":
            yield from (
                FindTask(self.uow)
                .find(
                    FindTaskQuery(
                        cmd.spec, cmd.order_by, cmd.reverse
                    )
                )
            )
            return
        elif cmd.type == "note":
            yield from (
                FindNote(self.uow)
                .find(
                    FindNoteQuery(
                        cmd.spec, cmd.order_by, cmd.reverse
                    )
                )
            )
            return
        else:
            raise InvalidValue("unknown entity type")


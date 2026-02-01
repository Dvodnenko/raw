from dataclasses import dataclass

from ...domain import (
    UnitOfWork, NotFound, EntityRef
)


@dataclass(frozen=True)
class RemoveCmd:
    id: int

class Remove:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def remove(self, cmd: RemoveCmd):
        with self.uow:
            exists = self.uow.intertype.resolve_type(cmd.id) is not None
            if not exists:
                raise NotFound(EntityRef(cmd.id))
            self.uow.intertype.remove(cmd.id)

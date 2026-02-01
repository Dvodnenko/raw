from dataclasses import dataclass

from ...domain import UnitOfWork, NotFound, EntityRef
from ..identifier import Identifier


@dataclass(frozen=True)
class RemoveCmd:
    identifier: Identifier

class Remove:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def remove(self, cmd: RemoveCmd):
        with self.uow:
            id = None
            
            if cmd.identifier.is_title:
                id = self.uow.intertype.resolve_id_by_title(cmd.identifier.value)
            else:
                id = int(cmd.identifier.value)

            if (not id) or (not self.uow.intertype.resolve_type(id)):
                raise NotFound(EntityRef(cmd.identifier.value))

            self.uow.intertype.remove(id)

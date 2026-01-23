from dataclasses import dataclass

from ...domain import (
    UnitOfWork, NotFoundError, EntityRef, EntityType
)


@dataclass(frozen=True)
class RemoveTaskCmd:
    id: int


class RemoveTask:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def remove(self, cmd: RemoveTaskCmd):
        with self.uow:
            task = self.uow.tasks.get_by_id(cmd.id)
            if not task:
                raise NotFoundError(EntityRef(EntityType.TASK, cmd.id))
            self.uow.tasks.remove(cmd.id)

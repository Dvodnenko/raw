from dataclasses import dataclass

from ...domain import (
    UnitOfWork, NotFound, EntityRef, EntityType
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
                raise NotFound(EntityRef(cmd.id))
            self.uow.tasks.remove(cmd.id)


@dataclass(frozen=True)
class RemoveEntityCmd:
    id: int

class RemoveEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def remove(self, cmd: RemoveEntityCmd):
        with self.uow:
            type = self.uow.intertype.resolve_type(cmd.id)

        if not type:
            raise NotFound(EntityRef(cmd.id))
        
        if type is EntityType.TASK:
            cmd = RemoveTaskCmd(cmd.id)
            RemoveTask(self.uow).remove(cmd)

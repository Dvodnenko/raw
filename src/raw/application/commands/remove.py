from dataclasses import dataclass

from ...domain import UnitOfWork


@dataclass(frozen=True)
class RemoveTaskCmd:
    id: int


class RemoveTask:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def remove(self, cmd: RemoveTaskCmd):
        with self.uow:
            self.uow.tasks.remove(cmd.id)

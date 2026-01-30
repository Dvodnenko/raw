from dataclasses import dataclass

from ...domain import UnitOfWork, EntityType
from .find import TaskView


@dataclass(frozen=True)
class FindEntityByIdQuery:
    id: int


class FindEntityById:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find_by_id(self, cmd: FindEntityByIdQuery):
        with self.uow:
            type = self.uow.resolver.resolve(cmd.id)

            if type is EntityType.TASK:
                task = self.uow.tasks.get_by_id(cmd.id)
                
                return TaskView(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    icon=task.icon,
                    parent_id=task.parent_id,
                    status=task.status,
                    deadline=task.deadline,
                )

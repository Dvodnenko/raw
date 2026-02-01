from dataclasses import dataclass
from typing import Any

from ....domain import UnitOfWork,InvalidValue
from .task import AddTask, AddTaskCmd


@dataclass(frozen=True)
class AddEntityCmd:
    type: str
    fields: dict[str, Any]

class AddEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add(self, cmd: AddEntityCmd):
        if cmd.type == "task":
            AddTask(self.uow).add(AddTaskCmd(**cmd.fields))
        else:
            raise InvalidValue("unknown entity type")
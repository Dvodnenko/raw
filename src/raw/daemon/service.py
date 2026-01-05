from enum import Enum

from .repository.cls import Repository
from .domain import build_entity, OperationNotFoundError
from .domain.schemes import (
    BaseScheme, CreationScheme, EditingScheme, DeletionScheme,
    FiltrationScheme)


class Service:

    def __init__(self, repo: Repository):
        self.repo = repo

    # Helpers

    class OperationType(Enum):
        DML = 0
        DQL = 1
    operations: dict[str, str] = {
        "dmls": {
            "create": "create",
            "add": "create",

            "edit": "edit",
            "update": "edit",
            "change": "edit",

            "delete": "delete",
            "remove": "delete",
            "rm": "delete",
        },
        "dqls": {
            "filter": "filter",
            "select": "filter",
        },
    }
    operation_to_scheme: dict[str, type[BaseScheme]] = {
        "create": CreationScheme,
        "edit": EditingScheme,
        "delete": DeletionScheme,
        "filter": FiltrationScheme,
    }

    @classmethod
    def get_operation_method_n_type(cls, name: str) -> tuple[str, OperationType]:
        if name in cls.operations["dmls"].keys():
            return (
                cls.operations["dmls"][name],
                cls.OperationType.DML
            )
        elif name in cls.operations["dqls"].keys():
            return (
                cls.operations["dqls"][name],
                cls.OperationType.DQL
            )
        raise OperationNotFoundError(name)

    # DMLs

    def create(self, data: CreationScheme):
        obj = build_entity(**data.parameters)
        self.repo.create(obj)
        return None

    def edit(self, data: EditingScheme):
        self.repo.edit(**data.resolve, **data.parameters)
        return None

    def delete(self, data: DeletionScheme):
        self.repo.delete(**data.resolve)
        return None

    # Queries

    def filter(self, data: FiltrationScheme):
        yield from self.repo.filter(data.filters)

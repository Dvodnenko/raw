from dataclasses import dataclass
from enum import Enum
from typing import Union


class EntityType(Enum):
    TASK = "task"

@dataclass(frozen=True)
class EntityRef:
    type: EntityType
    identity: Union[int, str]


class DomainError(Exception):
    """Base domain error class"""


## Existential Errors ##
@dataclass(init=False)
class AlreadyExistsError(DomainError):
    entity: EntityRef

    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"{entity.type.value} already exists: {entity.identity}")

@dataclass(init=False)
class NotFoundError(DomainError):
    entity: EntityRef

    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"{entity.type.value} not found: {entity.identity}")


## Tree Hierarchy-Related Errors ##
@dataclass
class InvariantViolationError(DomainError):
    ...


## Unexpected Error ##
@dataclass
class UnexpectedError(DomainError):
    ...


## Other ##

@dataclass
class PermissionDeniedError(DomainError):
    ...

@dataclass
class StorageUnavailableError(DomainError):
    ...

from dataclasses import dataclass
from enum import Enum
import re


class EntityType(Enum):
    TASK = "task"

@dataclass(frozen=True)
class EntityRef:
    type: EntityType
    id: int


class DomainError(Exception):
    """Base domain error class"""


## Existential Errors ##
@dataclass(init=False)
class AlreadyExistsError(DomainError):
    entity: EntityRef

    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"{entity.type.value} already exists: {entity.id}")

@dataclass(init=False)
class NotFoundError(DomainError):
    entity: EntityRef

    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"{entity.type.value} not found: {entity.id}")


## Tree Hierarchy-Related Errors ##
@dataclass
class InvariantViolationError(DomainError):
    ...


## Unexpected Error ##
@dataclass
class UnexpectedError(DomainError):
    ...

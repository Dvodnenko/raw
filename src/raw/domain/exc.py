from dataclasses import dataclass
from enum import Enum
from typing import Union, Any


class EntityType(Enum):
    TASK = "task"

@dataclass(frozen=True)
class EntityRef:
    type: EntityType
    identity: Union[int, str]


class DomainError(Exception):
    """Base domain error class"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AlreadyExists(DomainError):
    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"{entity.type.value} already exists: {entity.identity}")

class NotFound(DomainError):
    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"{entity.type.value} not found: {entity.identity}")

class InvalidValue(DomainError):
    ...

class InvalidState(DomainError):
    ...

class Unexpected(DomainError):
    ...

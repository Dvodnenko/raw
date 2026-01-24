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


class AlreadyExists(DomainError):
    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"{entity.type.value} already exists: {entity.identity}")

class NotFound(DomainError):
    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"{entity.type.value} not found: {entity.identity}")

class InvalidValue(DomainError):
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value
        super().__init__(f"invalid {field} value ({value})")

class InvalidState(DomainError):
    ...

class Unexpected(DomainError):
    ...

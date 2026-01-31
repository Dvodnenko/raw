from dataclasses import dataclass
from typing import Union

from .enums import EntityType


@dataclass(frozen=True)
class EntityRef:
    identity: Union[int, str]


class DomainError(Exception):
    """Base domain error class"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AlreadyExists(DomainError):
    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"already exists: {entity.identity}")

class NotFound(DomainError):
    def __init__(self, entity: EntityRef):
        self.entity = entity
        super().__init__(f"not found: {entity.identity}")

class InvalidValue(DomainError):
    ...

class InvalidState(DomainError):
    ...

class Unexpected(DomainError):
    ...

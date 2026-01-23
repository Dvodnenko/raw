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
@dataclass(init=False)
class ParentNotFoundError(DomainError):
    parent_name: str # that was provided

    def __init__(self, parent_name: str):
        self.parent_name = parent_name
        super().__init__(f"parent not found: {parent_name}")

@dataclass(init=False)
class InvalidTitlePatternError(DomainError):
    title: str # that was provided
    pattern: re.Pattern # correct & expected pattern

    def __init__(self, title: str, pattern: re.Pattern):
        self.title = title
        self.pattern = pattern
        super().__init__(
            f"invalid title: {title} (expected {self.pattern.pattern})")


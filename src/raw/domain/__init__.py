from .entities import Task, Entity
from .enums import TaskStatus
from .interfaces import TaskRepository, UnitOfWork
from .spec import Spec, FieldSpec, And, Or, Not, and_, or_
from .editors import TaskEditor
from .exc import (
    EntityRef,
    EntityType,
    DomainError,
    AlreadyExistsError,
    NotFoundError,
    InvariantViolationError,
    UnexpectedError,
    PermissionDeniedError,
    StorageUnavailableError,
)


__all__ = (
    ## Entity Types
    "Entity",
    "Task",

    ## Enums
    "TaskStatus",

    ## Interfaces
    "TaskRepository",
    "UnitOfWork",

    ## Queries' Specifications
    # Models
    "Spec",
    "FieldSpec",
    "And",
    "Or",
    "Not",

    # Methods
    "and_",
    "or_",

    ## Editors
    "TaskEditor",

    ## Errors
    # Base
    "DomainError",

    # Helper classes
    "EntityRef",
    "EntityType",

    # Special Errors
    "UnexpectedError",

    # Existential Errors
    "AlreadyExistsError",
    "NotFoundError",

    # Invariants Violations
    "InvariantViolationError",

    # Other
    "PermissionDeniedError",
    "StorageUnavailableError",
)

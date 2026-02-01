from .entities import Task, Entity
from .enums import TaskStatus, EntityType
from .interfaces import UnitOfWork, IntertypeRepository, TaskRepository
from .spec import Spec, FieldSpec, And, Or, Not, and_, or_, Operator
from .editors import TaskEditor
from .exc import (
    EntityRef,
    DomainError,
    AlreadyExists,
    NotFound,
    InvalidValue,
    InvalidState,
    Unexpected,
)


__all__ = (
    ## Entity Types
    "Entity",
    "Task",

    ## Enums
    "EntityType",
    "TaskStatus",

    ## Interfaces
    "UnitOfWork",
    "IntertypeRepository",
    "TaskRepository",

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

    # Enums
    "Operator",

    ## Editors
    "TaskEditor",

    ## Errors
    # Base
    "DomainError",

    # All Exceptions
    "AlreadyExists",
    "NotFound",
    "InvalidValue",
    "InvalidState",
    "Unexpected",

    # Helper Classes
    "EntityRef",
)

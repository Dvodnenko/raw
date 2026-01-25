from .entities import Task, Entity
from .enums import TaskStatus, EntityType
from .interfaces import EntityTypeResolver, UnitOfWork, TaskRepository
from .spec import Spec, FieldSpec, And, Or, Not, and_, or_
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
    "EntityTypeResolver",
    "UnitOfWork",
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

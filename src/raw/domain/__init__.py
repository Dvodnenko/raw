from .entities import Entity, Task, Note
from .enums import TaskStatus, EntityType
from .interfaces import UnitOfWork, IntertypeRepository, TaskRepository, NoteRepository
from .spec import Spec, FieldSpec, And, Or, Not, and_, or_, Operator
from .editors import TaskEditor, NoteEditor
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
    "Note",

    ## Enums
    "EntityType",
    "TaskStatus",

    ## Interfaces
    "UnitOfWork",
    "IntertypeRepository",
    "TaskRepository",
    "NoteRepository",

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
    "NoteEditor",

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

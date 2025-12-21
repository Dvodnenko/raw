from .entity import Entity
from .folder import Folder
from .session import Session
from .tag import Tag
from .task import Task
from .note import Note
from .enums import TaskStatus


ENTITIES: dict[str, type[Entity]] = {
    "entity": Entity,
    "folder": Folder,
    "session": Session,
    "tag": Tag,
    "task": Task,
    "note": Note
}

__all__ = (
    "Entity", "Folder", "Session", "Tag", 
    "Task", "TaskStatus", "Note", "ENTITIES",
)

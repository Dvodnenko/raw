import inspect

from .entity import Entity
from .folder import Folder
from .session import Session
from .tag import Tag
from .task import Task
from .note import Note


ENTITIES: dict[str, type[Entity]] = {
    "entity": Entity,
    "folder": Folder,
    "session": Session,
    "tag": Tag,
    "task": Task,
    "note": Note
}


def build_entity(**data):
    cls = ENTITIES[data.get("type")]
    params = inspect.signature(cls).parameters
    return cls(**{k:data.get(k) for k in params})

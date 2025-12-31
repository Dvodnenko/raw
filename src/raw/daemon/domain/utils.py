import inspect

import dateparser

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


def plural_to_singular(value: str):
    return value.removesuffix("s")


NONES = ("none", "null", "0")

def parse_datetime(value: str):
    if value.lower() in NONES:
        return None
    res = dateparser.parse(value)
    if res:
        return res.replace(microsecond=0)
    raise ValueError(f"cannot parse string '{value}'")

def parse_list(value: str, separator: str = ","):
    return value.split(separator)

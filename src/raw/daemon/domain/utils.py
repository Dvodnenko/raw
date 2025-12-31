import inspect
from dataclasses import fields

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

ENTITIES_COLUMNS = {
    name: fields(cls)
    for name, cls in ENTITIES.items()
}

FIELD_NAME_TO_ENTITY_NAME = {}

for name, fields_ in ENTITIES_COLUMNS.items():
    for field in fields_:
        if not field.name in FIELD_NAME_TO_ENTITY_NAME.keys():
            FIELD_NAME_TO_ENTITY_NAME.update({field.name: name})

ALL_FIELDS = [
    field for type in ENTITIES.values()
    for field in fields(type)
]

ALL_FIELDS_NAME = [
    field.name for field in ALL_FIELDS
]


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

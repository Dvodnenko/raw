import inspect
from dataclasses import fields
from typing import Any

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


def build_entity(**data):
    cls = ENTITIES[data.get("type")]
    params = inspect.signature(cls).parameters
    return cls(**{k:data.get(k) for k in params})


def plural_to_singular(value: str):
    return value.removesuffix("s")


NONES = ("none", "null", "0")

def parse_datetime(value: str):
    if value is None or value.lower() in NONES:
        return None
    res = dateparser.parse(value)
    if res:
        return res.replace(microsecond=0)
    raise ValueError(f"cannot parse string '{value}'")

def parse_list(value: str, separator: str = ","):
    return value.split(separator)


def resolve_entities_to_filter(
    filters: dict[str, list[Any]]
):
    entity_to_filter_map: dict[str, dict[str, list[Any]]] = {}
    for filter_name_and_op, values_list in filters.items():
        if "__" in filter_name_and_op: # then it's a complex expression
            entity = FIELD_NAME_TO_ENTITY_NAME[
                filter_name_and_op[0:filter_name_and_op.index("__")]]
        else:
            entity = FIELD_NAME_TO_ENTITY_NAME[filter_name_and_op]

        if entity_to_filter_map.get(entity):
            entity_to_filter_map[entity].update({filter_name_and_op: values_list})
        else:
            entity_to_filter_map[entity] = {filter_name_and_op: values_list}
    return entity_to_filter_map

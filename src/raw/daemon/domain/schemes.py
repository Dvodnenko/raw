"""
Data Transfering Protocols for each CRUD operation
"""

from dataclasses import fields
from datetime import datetime
from typing import get_origin, Any

from .entity import Entity
from .utils import parse_datetime, parse_list


def cast(dict_: dict[str, str], cls: type[Entity]) -> dict[str, Any]:
    allowed = {f.name: f for f in fields(cls)}
    result = {}

    for key, value in dict_.items():
        if allowed[key].name == "links": # links cannot be parsed dynamically
            result[key] = [int(v) for v in parse_list(value, ",")]
        elif allowed[key].type is datetime:
            result[key] = parse_datetime(value)
        elif (
            allowed[key].type is list or
            get_origin(allowed[key].type) is list
        ):
            result[key] = parse_list(value)
        else:
            result[key] = allowed[key].type(value)

    return result

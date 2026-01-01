"""
Data Transfering Protocols for each CRUD operation
"""

from dataclasses import dataclass, fields
from datetime import datetime
from typing import get_origin, Any

from .entity import Entity
from .utils import parse_datetime, parse_list, ENTITIES


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

def cast_filters(
    filters: dict[str, dict[str, list[Any]]],
):
    for entity_name, filters_ in filters.items():
        cls = ENTITIES[entity_name]
        allowed = {f.name: f for f in fields(cls)}
        result: dict[str, dict[str, list[Any]]] = {}
        for filter_name_and_op, values_list in filters_.items():
            if not result.get(entity_name):
                result[entity_name] = {}

            if "__" in filter_name_and_op:
                filter_name = filter_name_and_op[
                    0:filter_name_and_op.find("__")]
            else:
                filter_name = filter_name_and_op
            
            if allowed[filter_name].type is datetime:
                result[entity_name][filter_name_and_op] = [parse_datetime(v) for v in values_list]
            elif (
                allowed[filter_name].type is list or
                get_origin(allowed[filter_name].type) is list
            ):
                result[entity_name][filter_name_and_op] = [parse_list(v) for v in values_list]
            else:
                result[entity_name][filter_name_and_op] = [
                    allowed[filter_name].type(v) for v in values_list]

    return result


@dataclass
class BaseScheme:
    args: list[str]
    flags: list[str]
    kwargs: dict[str, list[str]]

    @property
    def kw_without_lists(self):
        result: dict[str, str] = {}
        for key, values_list in self.kwargs.items():
            result[key] = values_list[0]
        return result

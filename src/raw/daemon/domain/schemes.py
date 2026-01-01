"""
Data Transfering Protocols for each CRUD operation
"""

from dataclasses import dataclass, fields, field
from datetime import datetime
from typing import get_origin, Any

from .entity import Entity
from .utils import (
    parse_datetime, parse_list, ENTITIES, plural_to_singular,
    resolve_entities_to_filter
)
from .exc import MissingIdentifierError


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

@dataclass
class CreationScheme(BaseScheme):

    type: str = field(init=False)
    parameters: dict[str, str] = field(init=False)

    def __post_init__(self):
        self.type = plural_to_singular(self.args[0])
        self.parameters = self.kw_without_lists
        self.parameters["type"] = self.type
        self.parameters = cast(self.parameters, ENTITIES[self.type])

@dataclass
class EditingScheme(BaseScheme):
    identifier: str = field(init=False)
    parameters: dict[str, dict[str, list[Any]]] = field(init=False)

    def __post_init__(self):
        try:
            self.identifier = self.args[0]
        except IndexError:
            raise MissingIdentifierError()
        self.parameters = self.kwargs
        self.parameters = resolve_entities_to_filter(self.parameters)
        for entity_name, value in self.parameters.items():
            for edit_field_name, values_list in self.parameters[entity_name].items():
                self.parameters[entity_name][edit_field_name] = values_list[0]
            self.parameters[entity_name] = cast(value, ENTITIES[entity_name])

    @property
    def resolve(self):
        if self.identifier.isdigit():
            return {"id_": int(self.identifier)}
        else:
            return {"title_": self.identifier}

@dataclass
class DeletionScheme(BaseScheme):
    identifier: str = field(init=False)

    def __post_init__(self):
        self.identifier = self.args[0]

    @property
    def resolve(self):
        if self.identifier.isdigit():
            return {"id_": int(self.identifier)}
        else:
            return {"title_": self.identifier}

@dataclass
class FiltrationScheme(BaseScheme):
    filters: dict[str, dict[str, list[Any]]] = field(init=False)
    order_by: str | None = field(init=False)

    def __post_init__(self):
        self.order_by = self.kwargs.pop("orderby", None)
        self.filters = resolve_entities_to_filter(self.kwargs)
        self.filters = cast_filters(self.filters)


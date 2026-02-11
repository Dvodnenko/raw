import argparse

import jinja2

from ...shared import MISSING
from ...domain import InvalidValue
from ...application import FindEntity, FindEntityQuery
from ...infrastructure import UnitOfWorkSQL
from ...config import config
from ..resolvers import resolve_arg
from ..parsers import parse_infix


def handle_find_cmd(args: argparse.Namespace):
    types: str = args.types
    raw_filter = resolve_arg("specification", args.where)
    reverse: bool = args.r
    order_by = resolve_arg("orderby", args.orderby)
    sepby = resolve_arg("sepby", args.sepby)

    if order_by in (MISSING, None):
        order_by = None

    if sepby in (MISSING, None):
        sepby = None

    if raw_filter is MISSING:
        raw_filter = None

    spec = None
    if raw_filter:
        try:
            spec = parse_infix(raw_filter)
        except Exception as exc:
            raise InvalidValue("invalid filter") from exc

    cmd = FindEntityQuery(
        types=types,
        spec=spec,
        order_by=order_by or "id",
        reverse=reverse,
    )

    interactor = FindEntity(UnitOfWorkSQL(config["core"]["database"]))

    env = jinja2.Environment(
        autoescape=False,
        undefined=jinja2.StrictUndefined,
    )
    templates = {
        "task": env.from_string(config["output"]["formats"]["task"]),
        "note": env.from_string(config["output"]["formats"]["note"]),
        "session": env.from_string(config["output"]["formats"]["session"]),
        "folder": env.from_string(config["output"]["formats"]["folder"]),
    }

    gen = interactor.find(cmd)
    if sepby:
        first_entity = next(gen)
        print(templates[first_entity.type].render(obj=first_entity))
        last_value = getattr(first_entity, sepby)
        for obj in gen:
            if (new_value := getattr(obj, sepby)) != last_value:
                print()
                last_value = new_value
            print(templates[obj.type].render(obj=obj))
    else:
        for obj in gen:
            print(templates[obj.type].render(obj=obj))

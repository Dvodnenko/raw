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

    if order_by in (MISSING, None):
        order_by = None

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

    for obj in interactor.find(cmd):
        print(templates[obj.type].render(obj=obj))

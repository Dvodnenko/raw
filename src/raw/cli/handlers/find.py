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
    type: str = args.type.rstrip("s")
    raw_filter = resolve_arg("specification", args.where)
    reverse: bool = config["output"]["order"][type][1] != args.r
    order_by = resolve_arg("orderby", args.orderby)

    if order_by is MISSING:
        order_by = config["output"]["order"][type][0]

    if raw_filter is MISSING:
        raw_filter = None

    spec = None
    if raw_filter:
        try:
            spec = parse_infix(raw_filter)
        except Exception as exc:
            raise InvalidValue("invalid filter") from exc

    cmd = FindEntityQuery(
        type=type,
        spec=spec,
        order_by=order_by or "id",
        reverse=reverse,
    )
    interactor = FindEntity(UnitOfWorkSQL(config["core"]["database"]))

    env = jinja2.Environment(
        autoescape=False,
        undefined=jinja2.StrictUndefined,
    )
    template = env.from_string(config["output"]["formats"][type])

    for obj in interactor.find(cmd):
        print(template.render(obj=obj))

import argparse

import jinja2

from ...domain import InvalidValue
from ...application import FindEntity, FindEntityQuery
from ...infrastructure import UnitOfWorkSQL
from ...config import config
from ..resolvers import resolve_arg
from ..parsers import parse_infix


def handle_find_cmd(args: argparse.Namespace):
    raw_filter = resolve_arg("specification", args.where)
    order_by = resolve_arg("orderby", args.orderby)

    spec = None
    if raw_filter:
        try:
            spec = parse_infix(raw_filter)
        except Exception as exc:
            raise InvalidValue("invalid filter") from exc

    cmd = FindEntityQuery(
        type=args.type.rstrip("s"),
        spec=spec,
        order_by=order_by or "id",
        reverse=args.r,
    )
    interactor = FindEntity(UnitOfWorkSQL(config["core"]["database"]))

    env = jinja2.Environment(
        autoescape=False,
        undefined=jinja2.StrictUndefined,
    )
    template = env.from_string(config["formats"][args.type.rstrip("s")])

    for obj in interactor.find(cmd):
        print(template.render(obj=obj))

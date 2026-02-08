import argparse

import jinja2

from ...shared import MISSING
from ...application import GetActiveSessions, GetActiveSessionQuery
from ...infrastructure import UnitOfWorkSQL
from ...config import config
from ..resolvers import resolve_arg


def handle_gas_cmd(args: argparse.Namespace):
    order_by = resolve_arg("orderby", args.orderby)

    if order_by is MISSING:
        order_by = config["output"]["order"]["session"][0]

    cmd = GetActiveSessionQuery(
        order_by=order_by or "id",
        reverse=args.r,
    )
    interactor = GetActiveSessions(UnitOfWorkSQL(config["core"]["database"]))

    env = jinja2.Environment(
        autoescape=False,
        undefined=jinja2.StrictUndefined,
    )
    template = env.from_string(config["output"]["formats"]["session"])

    for obj in interactor.get_active_sessions(cmd):
        print(template.render(obj=obj))

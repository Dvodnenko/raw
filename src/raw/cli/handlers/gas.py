import argparse

from ...application import GetActiveSessions, GetActiveSessionQuery
from ...infrastructure import UnitOfWorkSQL
from ...config import config
from ..resolvers import resolve_arg


def handle_gas_cmd(args: argparse.Namespace):
    order_by = resolve_arg("orderby", args.orderby)

    cmd = GetActiveSessionQuery(
        order_by=order_by or "id",
        reverse=args.r,
    )
    interactor = GetActiveSessions(UnitOfWorkSQL(config["core"]["database"]))

    for entity in interactor.get_active_sessions(cmd):
        print(f"#{entity.id} {entity.title}")

import argparse

from ...application import GetActiveSessions, GetActiveSessionQuery
from ...infrastructure import UnitOfWorkSQL
from ...config import DB_PATH
from ..resolvers import resolve_arg


def handle_gas_cmd(args: argparse.Namespace):
    order_by = resolve_arg("orderby", args.orderby)

    cmd = GetActiveSessionQuery(
        order_by=order_by or "id",
        reverse=args.r,
    )
    interactor = GetActiveSessions(UnitOfWorkSQL(DB_PATH))

    for entity in interactor.get_active_sessions(cmd):
        print(f"#{entity.id} {entity.title}")

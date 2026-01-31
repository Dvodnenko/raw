import argparse

from ...domain import InvalidValue
from ...application import FindEntity, FindEntityQuery
from ...infrastructure import UnitOfWorkSQL
from ...config import DB_PATH
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
        type=args.type.strip("s"),
        spec=spec,
        order_by=order_by or "id",
        reverse=args.r,
    )
    interactor = FindEntity(UnitOfWorkSQL(DB_PATH))

    for entity in interactor.find(cmd):
        print(f"#{entity.id} {entity.title}")

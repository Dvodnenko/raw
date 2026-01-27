import argparse

from ...config import DB_PATH
from ..resolvers import resolve_arg, parse_datetime, parse_enum


def handle_edit_cmd(args: argparse.Namespace):
    from ...domain import TaskStatus
    from ...application import EditEntity, EditEntityCmd
    from ...infrastructure import UnitOfWorkSQL
    
    cmd_kwargs = {}

    id: int = args.id
    title = resolve_arg(args.title)
    description = resolve_arg(args.description)
    icon = resolve_arg(args.icon)
    status = parse_enum(resolve_arg(args.status), TaskStatus, "status")
    deadline = parse_datetime(resolve_arg(args.deadline), "deadline")

    if title: cmd_kwargs.update({"title": title})
    if description: cmd_kwargs.update({"description": description})
    if icon: cmd_kwargs.update({"icon": icon})
    if status: cmd_kwargs.update({"status": status})
    if deadline: cmd_kwargs.update({"deadline": deadline})

    cmd = EditEntityCmd(
        id=id,
        fields=cmd_kwargs
    )
    interactor = EditEntity(UnitOfWorkSQL(DB_PATH))

    interactor.edit(cmd)

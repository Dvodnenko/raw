import argparse

from ...config import DB_PATH
from ..resolvers import resolve_arg, parse_datetime, parse_enum


def handle_add_cmd(args: argparse.Namespace):
    from ...domain import TaskStatus
    from ...application import AddEntity, AddEntityCmd
    from ...infrastructure import UnitOfWorkSQL
    
    cmd_kwargs = {}

    type: str = args.type
    title = resolve_arg("title", args.title)
    description = resolve_arg("description", args.description)
    icon = resolve_arg("icon", args.icon)
    status = parse_enum(resolve_arg("status", args.status), TaskStatus, "status")
    deadline = parse_datetime(resolve_arg("deadline", args.deadline), "deadline")
    content = resolve_arg("content", args.content)

    if title: cmd_kwargs.update({"title": title})
    if description: cmd_kwargs.update({"description": description})
    if icon: cmd_kwargs.update({"icon": icon})
    if status: cmd_kwargs.update({"status": status})
    if deadline: cmd_kwargs.update({"deadline": deadline})
    if content: cmd_kwargs.update({"content": content})

    cmd = AddEntityCmd(
        type=type,
        fields=cmd_kwargs
    )
    interactor = AddEntity(UnitOfWorkSQL(DB_PATH))

    interactor.add(cmd)

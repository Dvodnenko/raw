import argparse

from ...config import DB_PATH
from ..resolvers import resolve_arg, parse_datetime, parse_enum


def handle_add_cmd(args: argparse.Namespace):
    from ...application import AddEntity, AddEntityCmd
    from ...infrastructure import UnitOfWorkSQL
    
    cmd_kwargs = {}

    type: str = args.type
    title = resolve_arg("title", args.title)
    description = resolve_arg("description", args.description)
    icon = resolve_arg("icon", args.icon)

    ## Task Options
    status = resolve_arg("status", args.status)
    deadline = parse_datetime(resolve_arg("deadline", args.deadline), "deadline")
    ## Note Options
    content = resolve_arg("content", args.content)
    ## Session Options
    message = resolve_arg("message", args.message)
    summary = resolve_arg("summary", args.summary)
    started_at = parse_datetime(resolve_arg("started_at", args.started_at), "started_at")
    ended_at = parse_datetime(resolve_arg("ended_at", args.ended_at), "ended_at")

    if title: cmd_kwargs.update({"title": title})
    if description: cmd_kwargs.update({"description": description})
    if icon: cmd_kwargs.update({"icon": icon})
    if status: cmd_kwargs.update({"status": status})
    if deadline: cmd_kwargs.update({"deadline": deadline})
    if content: cmd_kwargs.update({"content": content})
    if message: cmd_kwargs.update({"message": message})
    if summary: cmd_kwargs.update({"summary": summary})
    if started_at: cmd_kwargs.update({"started_at": started_at})
    if ended_at: cmd_kwargs.update({"ended_at": ended_at})

    cmd = AddEntityCmd(
        type=type,
        fields=cmd_kwargs
    )
    interactor = AddEntity(UnitOfWorkSQL(DB_PATH))

    interactor.add(cmd)

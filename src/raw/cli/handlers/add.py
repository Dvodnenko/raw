import argparse

from ...shared import MISSING
from ...config import config
from ..resolvers import resolve_arg, parse_datetime


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

    if title is not MISSING: cmd_kwargs.update({"title": title})
    if description is not MISSING: cmd_kwargs.update({"description": description})
    if icon is not MISSING: cmd_kwargs.update({"icon": icon})
    if status is not MISSING: cmd_kwargs.update({"status": status})
    if deadline is not MISSING: cmd_kwargs.update({"deadline": deadline})
    if content is not MISSING: cmd_kwargs.update({"content": content})
    if message is not MISSING: cmd_kwargs.update({"message": message})
    if summary is not MISSING: cmd_kwargs.update({"summary": summary})
    if started_at is not MISSING: cmd_kwargs.update({"started_at": started_at})
    if ended_at is not MISSING: cmd_kwargs.update({"ended_at": ended_at})

    cmd = AddEntityCmd(
        type=type,
        fields=cmd_kwargs
    )
    interactor = AddEntity(UnitOfWorkSQL(config["core"]["database"]))

    interactor.add(cmd)

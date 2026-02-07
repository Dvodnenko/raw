import argparse

from ...config import config
from ..resolvers import resolve_arg, parse_datetime


def handle_start_cmd(args: argparse.Namespace):
    from ...application import StartSession, StartSessionCmd
    from ...infrastructure import UnitOfWorkSQL
    
    cmd_kwargs = {}

    title = resolve_arg("title", args.title)
    description = resolve_arg("description", args.description)
    icon = resolve_arg("icon", args.icon)

    ## Session Options
    message = resolve_arg("message", args.message)
    summary = resolve_arg("summary", args.summary)
    started_at = parse_datetime(resolve_arg("started_at", args.started_at), "started_at")
    ended_at = parse_datetime(resolve_arg("ended_at", args.ended_at), "ended_at")

    if title: cmd_kwargs.update({"title": title})
    if description: cmd_kwargs.update({"description": description})
    if icon: cmd_kwargs.update({"icon": icon})
    if message: cmd_kwargs.update({"message": message})
    if summary: cmd_kwargs.update({"summary": summary})
    if started_at: cmd_kwargs.update({"started_at": started_at})
    if ended_at: cmd_kwargs.update({"ended_at": ended_at})

    cmd = StartSessionCmd(
        **cmd_kwargs,
    )
    interactor = StartSession(UnitOfWorkSQL(config["core"]["database"]))

    interactor.start(cmd)

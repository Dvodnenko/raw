import argparse

from ...config import config
from ..resolvers import resolve_arg, parse_datetime


def handle_edit_cmd(args: argparse.Namespace):
    from ...domain import NotFound, EntityRef
    from ...application import (
        EditEntity, EditEntityCmd, FindEntityByIdentifier,
        FindEntityByIdentifierQuery, Identifier
    )
    from ...infrastructure import UnitOfWorkSQL
    
    cmd_kwargs = {}

    identifier = Identifier(args.identifier)

    # check if the entity exists. if so - grab values for initial text in editor
    query = FindEntityByIdentifierQuery(identifier)
    entity = FindEntityByIdentifier(UnitOfWorkSQL(config["core"]["database"])).find(query)
    if not entity:
        raise NotFound(EntityRef(identifier.value))

    title = resolve_arg("title", args.title, entity.title)
    description = resolve_arg("description", args.description, entity.description)
    icon = resolve_arg("icon", args.icon, entity.icon)

    if title: cmd_kwargs.update({"title": title})
    if description: cmd_kwargs.update({"description": description})
    if icon: cmd_kwargs.update({"icon": icon})

    match entity.type:
        case "task":
            status = resolve_arg("status", args.status, entity.status)
            deadline = parse_datetime(resolve_arg("deadline", args.deadline, entity.deadline), "deadline")

            if status: cmd_kwargs.update({"status": status})
            if deadline: cmd_kwargs.update({"deadline": deadline})
        case "note":
            content = resolve_arg("content", args.content, entity.content)
            if content: cmd_kwargs.update({"content": content})
        case "session":
            message = resolve_arg("message", args.message, entity.message)
            summary = resolve_arg("summary", args.summary, entity.summary)
            started_at = parse_datetime(resolve_arg("started_at", args.started_at, entity.started_at), "started_at")
            ended_at = parse_datetime(resolve_arg("ended_at", args.ended_at, entity.ended_at), "ended_at")

            if message: cmd_kwargs.update({"message": message})
            if summary: cmd_kwargs.update({"summary": summary})
            if started_at: cmd_kwargs.update({"started_at": started_at})
            if ended_at: cmd_kwargs.update({"ended_at": ended_at})

    cmd = EditEntityCmd(
        identifier=identifier,
        fields=cmd_kwargs
    )
    interactor = EditEntity(UnitOfWorkSQL(config["core"]["database"]))

    interactor.edit(cmd)

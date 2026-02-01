import argparse

from ...config import DB_PATH
from ..resolvers import resolve_arg, parse_datetime, parse_enum


def handle_edit_cmd(args: argparse.Namespace):
    from ...domain import TaskStatus, NotFound, EntityRef
    from ...application import (
        EditEntity, EditEntityCmd, FindEntityByIdentifier,
        FindEntityByIdentifierQuery, Identifier
    )
    from ...infrastructure import UnitOfWorkSQL
    
    cmd_kwargs = {}

    identifier = Identifier(args.identifier)

    # check if the entity exists. if so - grab values for initial text in editor
    query = FindEntityByIdentifierQuery(identifier)
    entity = FindEntityByIdentifier(UnitOfWorkSQL(DB_PATH)).find(query)
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
            status = parse_enum(resolve_arg("status", args.status, entity.status), TaskStatus, "status")
            deadline = parse_datetime(resolve_arg("deadline", args.deadline, entity.deadline), "deadline")

            if status: cmd_kwargs.update({"status": status})
            if deadline: cmd_kwargs.update({"deadline": deadline})
        case "note":
            content = resolve_arg("content", args.content, entity.content)
            if content: cmd_kwargs.update({"content": content})

    cmd = EditEntityCmd(
        identifier=identifier,
        fields=cmd_kwargs
    )
    interactor = EditEntity(UnitOfWorkSQL(DB_PATH))

    interactor.edit(cmd)

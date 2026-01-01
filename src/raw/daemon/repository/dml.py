from typing import Sequence
from dataclasses import asdict

from sqlalchemy import (
    Connection,
    insert,
    update,
    delete as sa_delete,
    select
)

from ..domain import Entity, MissingIdentifierError
from ..database.mappings import (
    TABLES, TABLES_COLUMNS,
    entity_table, link_table
)


def create(conn: Connection, obj: Entity):
    kwargs = asdict(obj)
    columns = {*kwargs.keys()}.difference("id")
    entity_values = {c: kwargs[c] 
        for c in columns.intersection(TABLES_COLUMNS["entity"].keys())}
    this_values = {c: kwargs[c] 
        for c in columns.intersection(TABLES_COLUMNS[obj.type].keys())}
    links = kwargs.pop("links", None)

    stmt1 = (
        insert(entity_table)
        .values(**entity_values)
        .returning(entity_table.c.id)
    )
    entity_part = conn.execute(stmt1).one()

    this_values["id"] = entity_part.id
    stmt2 = (
        insert(TABLES[obj.type])
        .values(**this_values)
    )
    conn.execute(stmt2)

    if links:
        link_entity(conn, entity_part.id, links)
    
    return None

def link_entity(conn: Connection, id: int, ids: Sequence[int]):
    stmt1 = sa_delete(link_table).where(link_table.c.from_id == id)
    conn.execute(stmt1)

    stmt2 = insert(link_table)
    conn.execute(
        stmt2,
        [
            {"from_id": id, "to_id": to_id} 
            for to_id in ids
        ]
    )
    return None

def edit(conn: Connection, id_: int = None, title_: str = None, **kwargs):

    if bool(id_) == bool(title_) == False:
        raise MissingIdentifierError()

    entities_kwargs = kwargs.pop("entity", None)
    
    if "links" in entities_kwargs.keys():
        links = entities_kwargs.pop("links")
    else:
        links = None

    if entities_kwargs:
        stmt1 = (
            update(entity_table)
            .values(**entities_kwargs)
            .returning(entity_table)
        )
    else:
        stmt1 = (
            select(entity_table)
        )

    if id_:
        stmt1 = stmt1.where(entity_table.c.id == id_)
    else:
        stmt1 = stmt1.where(entity_table.c.title == title_)

    entity_row = conn.execute(stmt1).one()
    table_name = entity_row.type
    table = TABLES[table_name]
    this_kwargs = kwargs.pop(table_name, None)

    if this_kwargs:
        stmt2 = (
            update(table)
            .values(**this_kwargs)
            .returning(table)
        )
    else:
        stmt2 = (
            select(table)
        )

    stmt2 = stmt2.where(table.c.id == entity_row.id)
    conn.execute(stmt2)

    if links:
        link_entity(conn, entity_row.id, links)

    return None

def delete(conn: Connection, id_: int = None, title_: str = None):
    if bool(id_) == bool(title_) == False:
        raise MissingIdentifierError()

    stmt1 = (
        sa_delete(entity_table)
        .returning(
            entity_table.c.title,
            entity_table.c.type
        )
    )

    if id_:
        stmt1 = stmt1.where(entity_table.c.id == id_)
    else:
        stmt1 = stmt1.where(entity_table.c.title == title_)

    entity_row = conn.execute(stmt1).one()
    table = TABLES[entity_row.type]
    stmt2 = sa_delete(table)

    if id_:
        stmt2 = stmt2.where(table.c.id == id_)
    else:
        stmt2 = stmt2.where(table.c.title == title_)

    conn.execute(stmt2)

    return None

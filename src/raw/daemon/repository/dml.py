from typing import Sequence
from dataclasses import asdict

from sqlalchemy import (
    Connection,
    insert,
    update,
    delete as sa_delete,
    select
)

from ..entities import build_entity, Entity
from ..database.mappings import (
    TABLES, TABLES_COLUMNS,
    entity_table, link_table
)
from .assemblers import resolve_tables_to_filter


def create(conn: Connection, obj: Entity):
    kwargs = asdict(obj)
    columns = {*kwargs.keys()}.difference("id")
    entity_values = {c: kwargs[c] 
        for c in columns.intersection(TABLES_COLUMNS["entity"].keys())}
    this_values = {c: kwargs[c] 
        for c in columns.intersection(TABLES_COLUMNS[obj.type].keys())}
    links: list[int] | None = kwargs.pop("link", None)
    
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
    kwargs["id"] = this_values["id"]
    if links:
        link_entity(conn, entity_part.id, links)
    
    return build_entity(**kwargs)

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
    return

def edit(conn: Connection, id: int, **kwargs):

    links: list[int] = kwargs.pop("link", [])
    kwargs = resolve_tables_to_filter(kwargs)
    entities_kwargs = kwargs.pop("entity", None)

    if entities_kwargs:
        stmt1 = (
            update(entity_table)
            .where(entity_table.c.id == id)
            .values(**entities_kwargs)
            .returning(
                entity_table.c.type,
                entity_table.c.parent_id,
                entity_table.c.title,
                entity_table.c.description,
                entity_table.c.styles,
                entity_table.c.icon,
            )
        )
    else:
        stmt1 = (
            select(
                entity_table.c.type,
                entity_table.c.parent_id,
                entity_table.c.title,
                entity_table.c.description,
                entity_table.c.styles,
                entity_table.c.icon,
            )
            .where(entity_table.c.id == id)
        )

    entity_row = conn.execute(stmt1).mappings().one()
    table_name = entity_row["type"]+"s"
    table = TABLES[table_name]
    this_kwargs = kwargs.pop(table_name, None)

    if this_kwargs:
        stmt2 = (
            update(table)
            .where(table.c.id == id)
            .values(**this_kwargs)
            .returning(table)
        )
    else:
        stmt2 = (
            select(table)
            .where(table.c.id == id)
        )

    this_row = conn.execute(stmt2).mappings().one()
    
    if links:
        link_entity(conn, this_row["id"], links)

    return build_entity(**entity_row, **this_row)

def delete(conn: Connection, id: int):
    stmt1 = (
        sa_delete(entity_table)
        .where(entity_table.c.id == id)
        .returning(
            entity_table.c.title,
            entity_table.c.type
        )
    )
    entity_row = conn.execute(stmt1).one()
    table = TABLES[entity_row.type]
    stmt2 = sa_delete(table).where(table.c.id == id)
    conn.execute(stmt2)

    return None

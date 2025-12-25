from typing import Sequence

from sqlalchemy import (
    Connection,
    insert,
    update as sa_update,
    delete as sa_delete,
    select
)

from ..database.mappings import (
    TABLES, TABLES_COLUMNS,
    entities_table, links_table
)
from .assemblers import build_entity, resolve_tables_to_filter, build_entity


def create(conn: Connection, table: str, **kwargs):
    columns = {*kwargs.keys()}.difference("id")
    entity_values = {c: kwargs[c] 
        for c in columns.intersection(TABLES_COLUMNS["entities"].keys())}
    this_values = {c: kwargs[c] 
        for c in columns.intersection(TABLES_COLUMNS[table].keys())}
    links: list[int] | None = kwargs.pop("links", None)
    
    stmt1 = (
        insert(entities_table)
        .values(**entity_values)
        .returning(entities_table.c.id)
    )
    entity_part = conn.execute(stmt1).one()

    this_values["id"] = entity_part.id
    stmt2 = (
        insert(TABLES[table])
        .values(**this_values)
    )
    conn.execute(stmt2)
    kwargs["id"] = this_values["id"]
    if links:
        link_entity(conn, entity_part.id, links)
    
    yield build_entity(**kwargs)

def link_entity(conn: Connection, id: int, ids: Sequence[int]):
    stmt1 = sa_delete(links_table).where(links_table.c.from_id == id)
    conn.execute(stmt1)

    stmt2 = insert(links_table)
    conn.execute(
        stmt2,
        [
            {"from_id": id, "to_id": to_id} 
            for to_id in ids
        ]
    )
    return

def update(conn: Connection, id: int, **kwargs):

    links: list[int] = kwargs.pop("links", [])
    kwargs = resolve_tables_to_filter(kwargs)
    entities_kwargs = kwargs.pop("entities", None)

    if entities_kwargs:
        stmt1 = (
            sa_update(entities_table)
            .where(entities_table.c.id == id)
            .values(**entities_kwargs)
            .returning(
                entities_table.c.type,
                entities_table.c.parent_id,
                entities_table.c.title,
                entities_table.c.description,
                entities_table.c.styles,
                entities_table.c.icon,
            )
        )
    else:
        stmt1 = (
            select(
                entities_table.c.type,
                entities_table.c.parent_id,
                entities_table.c.title,
                entities_table.c.description,
                entities_table.c.styles,
                entities_table.c.icon,
            )
            .where(entities_table.c.id == id)
        )

    entity_row = conn.execute(stmt1).mappings().one()
    table_name = entity_row["type"]+"s"
    table = TABLES[table_name]
    this_kwargs = kwargs.pop(table_name, None)

    if this_kwargs:
        stmt2 = (
            sa_update(table)
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

from typing import Sequence

from sqlalchemy import (
    Connection,
    insert,
    update as sa_update,
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
        next(link_entity(conn, entity_part.id, links))
    
    yield build_entity(**kwargs)

def link_entity(conn: Connection, id: int, ids: Sequence[int]):
    stmt = insert(links_table)
    conn.execute(
        stmt,
        [
            {"from_id": id, "to_id": to_id} 
            for to_id in ids
        ]
    )
    yield

def update(conn: Connection, id: int, **kwargs):

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
    this_kwargs = kwargs.pop(table_name)

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
    return build_entity(**entity_row, **this_row)

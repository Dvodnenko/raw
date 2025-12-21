import inspect
from typing import Sequence

from sqlalchemy import Connection, insert, select

from .database.mappings import (
    TABLES, TABLES_COLUMNS, TABLES_COLUMNS_NAMES,
    entities_table, links_table, folders_table, notes_table, 
    sessions_table, tags_table, tasks_table
)
from .entities import ENTITIES


def build_entity(**data):
    cls = ENTITIES[data.pop("type")]
    params = inspect.signature(cls).parameters
    return cls(**{k:data.get(k) for k in params})

def create(conn: Connection, table: str, **kwargs):
    cls = ENTITIES[table.rstrip("s")]
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

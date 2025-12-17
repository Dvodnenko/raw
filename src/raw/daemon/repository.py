from typing import Sequence

from sqlalchemy import Connection, insert, select

from .database.mappings import (
    TABLES, TABLES_COLUMNS, TABLES_COLUMNS_NAMES,
    entities_table, links_table, folders_table, notes_table, 
    sessions_table, tags_table, tasks_table
)


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

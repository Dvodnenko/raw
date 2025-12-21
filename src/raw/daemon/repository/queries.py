from sqlalchemy import Connection, select

from ..database.mappings import (
    entities_table, sessions_table, 
    tasks_table, notes_table, links_table
)


def fetch_entities_batch(conn: Connection, limit: int, offset: int):
    stmt = (
        select(
            entities_table.c.id,
            entities_table.c.type,
            entities_table.c.title,
        )
        .order_by(entities_table.c.id)
        .limit(limit)
        .offset(offset)
    )
    return conn.execute(stmt).mappings().all()

def enrich_entities(conn: Connection, ids: list[int]):
    stmt = (
        select(
            entities_table.c.id,
            entities_table.c.type,
            entities_table.c.title,

            sessions_table.c.start,
            sessions_table.c.end,
            sessions_table.c.summary,

            tasks_table.c.deadline,
            tasks_table.c.status,

            notes_table.c.content,
        )
        .where(entities_table.c.id.in_(ids))
        .outerjoin(sessions_table, sessions_table.c.id == entities_table.c.id)
        .outerjoin(tasks_table, tasks_table.c.id == entities_table.c.id)
        .outerjoin(notes_table, notes_table.c.id == entities_table.c.id)
        .order_by(entities_table.c.id)
    )

    return conn.execute(stmt).mappings().all()

def fetch_outgoing_links(conn: Connection, from_ids: list[int]):
    stmt = (
        select(
            entities_table.c.id,
            entities_table.c.type,
            entities_table.c.parent_id,
            entities_table.c.title,
            entities_table.c.description,
            entities_table.c.styles,
            entities_table.c.icon,

            links_table.c.from_id,

            sessions_table.c.start,
            sessions_table.c.end,
            sessions_table.c.summary,

            tasks_table.c.deadline,
            tasks_table.c.status,

            notes_table.c.content,
        )
        .where(links_table.c.from_id.in_(from_ids))
        .join(entities_table, entities_table.c.id == links_table.c.to_id)
        .outerjoin(sessions_table, sessions_table.c.id == entities_table.c.id)
        .outerjoin(tasks_table, tasks_table.c.id == entities_table.c.id)
        .outerjoin(notes_table, notes_table.c.id == entities_table.c.id)
        .order_by(links_table.c.from_id)
    )

    return conn.execute(stmt).mappings().all()

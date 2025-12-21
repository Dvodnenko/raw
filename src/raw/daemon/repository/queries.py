from sqlalchemy import Connection, select

from ..database.mappings import entities_table


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

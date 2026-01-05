from typing import Any
from dataclasses import fields

from sqlalchemy import Connection, Select, Table, select, or_

from ..database.mappings import (
    entity_table, session_table, 
    task_table, note_table, link_table,
    TABLES, TABLE_TO_ENTITY
)
from ..domain import Entity
from .assemblers import attach_links


def fetch_entities_batch(
    conn: Connection,
    limit: int,
    offset: int,
    filters: dict[str, list[Any]] = {}
):
    stmt = (
        select(
            entity_table.c.id,
            entity_table.c.type,
            entity_table.c.parent_id,
            entity_table.c.title,
            entity_table.c.description,
            entity_table.c.styles,
            entity_table.c.icon,
        )
        .order_by(entity_table.c.id)
        .limit(limit)
        .offset(offset)
    )
    if filters:
        stmt = apply_filters(stmt, filters, entity_table, Entity)
    return conn.execute(stmt).mappings().all()

def enrich_entities(
    conn: Connection,
    ids: list[int],
    filters: dict[str, dict[str, list[Any]]] = {}
):
    subq = (
        select(
            entity_table.c.id,
            entity_table.c.type,
            entity_table.c.parent_id,
            entity_table.c.title,
            entity_table.c.description,
            entity_table.c.styles,
            entity_table.c.icon,

            session_table.c.start,
            session_table.c.end,
            session_table.c.summary,

            task_table.c.deadline,
            task_table.c.status,

            note_table.c.content,
        )
        .where(entity_table.c.id.in_(ids))
        .outerjoin(session_table, session_table.c.id == entity_table.c.id)
        .outerjoin(task_table, task_table.c.id == entity_table.c.id)
        .outerjoin(note_table, note_table.c.id == entity_table.c.id)
        .order_by(entity_table.c.id)
        .subquery(name="subq_1")
    )

    query = select(subq)

    if filters:
        for table_name, filters_ in filters.items():
            query = apply_filters(
                query,
                filters_,
                subq,
                TABLE_TO_ENTITY[TABLES[table_name]]
            )

    return conn.execute(query).mappings().all()

def fetch_outgoing_links(conn: Connection, from_ids: list[int]):
    stmt = (
        select(
            entity_table.c.id,
            entity_table.c.type,
            entity_table.c.parent_id,
            entity_table.c.title,
            entity_table.c.description,
            entity_table.c.styles,
            entity_table.c.icon,

            link_table.c.from_id,

            session_table.c.start,
            session_table.c.end,
            session_table.c.summary,

            task_table.c.deadline,
            task_table.c.status,

            note_table.c.content,
        )
        .where(link_table.c.from_id.in_(from_ids))
        .join(entity_table, entity_table.c.id == link_table.c.to_id)
        .outerjoin(session_table, session_table.c.id == entity_table.c.id)
        .outerjoin(task_table, task_table.c.id == entity_table.c.id)
        .outerjoin(note_table, note_table.c.id == entity_table.c.id)
        .order_by(link_table.c.from_id)
    )

    return conn.execute(stmt).mappings().all()

OPERATORS = {
    "eq": lambda col, val: col == val,
    "ne": lambda col, val: col != val,
    "gt": lambda col, val: col > val,
    "lt": lambda col, val: col < val,
    "ge": lambda col, val: col >= val,
    "le": lambda col, val: col <= val,
    "like": lambda col, val: col.like(val),
    "notlike": lambda col, val: col.notlike(val),
    "ilike": lambda col, val: col.ilike(val),
    "notilike": lambda col, val: col.notilike(val),
    "in": lambda col, val: col.in_(val if isinstance(val, list) else [val]),
    "notin": lambda col, val: col.notin_(val if isinstance(val, list) else [val]),
}

def apply_filters(
    query: Select,
    filters: dict[str, list[Any]],
    table: Table,
    cls: type[Entity] = Entity,
):
    complex_expressions = []
    allowed = {f.name: f for f in fields(cls)}

    for key, value in filters.items():
        if "__" in key:
            field, op = key.split("__", 1)
        else:
            field, op = key, "eq"
        if not field in allowed.keys():
            continue
        column = getattr(table.c, field)
        if op in OPERATORS:
            expression = or_(
                OPERATORS[op](column, val)
                for val in value
            )
            complex_expressions.append(expression)

    if complex_expressions:
        query = query.where(*complex_expressions)

    return query

## Final APIs

def get_all(
    conn: Connection, 
    batch_size=100, 
    type: str = None, 
    ids: list[int] = None
):
    offset = 0

    while True:
        base = fetch_entities_batch(
            conn, batch_size, offset,
            type=type, ids=ids)
        if not base:
            break

        ids = [row["id"] for row in base]

        entities = enrich_entities(conn, ids)
        links = fetch_outgoing_links(conn, ids)

        yield from attach_links(entities, links)

        offset += batch_size

def filter(
    conn: Connection, 
    filters: dict[str, dict[str, list[Any]]],
):
    offset = 0
    batch_size = 100
    entity_only_filters = filters.pop("entity", {})

    while True:
        base = fetch_entities_batch(
            conn,
            batch_size,
            offset,
            entity_only_filters
        )
        if not base:
            break

        ids = [row["id"] for row in base]

        entities = enrich_entities(conn, ids, filters)
        links = fetch_outgoing_links(conn, ids)

        yield from attach_links(entities, links)

        offset += batch_size

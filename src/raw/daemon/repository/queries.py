from typing import Any
from datetime import datetime
from dataclasses import fields

from sqlalchemy import Connection, Select, Table, select

from ..database.mappings import (
    entities_table, sessions_table, 
    tasks_table, notes_table, links_table,
    TABLES, TABLE_TO_ENTITY
)
from ..funcs import cast_datetime
from ..entities import Entity
from .assemblers import attach_links


def fetch_entities_batch(
    conn: Connection,
    limit: int,
    offset: int,
    filters: dict[str, tuple[Any]] = {}
):
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
    if filters:
        stmt = apply_filters(stmt, filters, entities_table, Entity)
    return conn.execute(stmt).mappings().all()

def enrich_entities(
    conn: Connection,
    ids: list[int],
    filters: dict[str, dict[str, tuple[Any]]] = {}
):
    subq = (
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
    filters: dict[str, tuple[Any]],
    table: Table,
    cls: type[Entity] = Entity,
):
    simple_kwargs = {}
    complex_expressions = []
    allowed = {f.name: f for f in fields(cls)}

    for key, value in filters.items():
        if "__" in key:
            field, op = key.split("__", 1)
            if not field in allowed.keys():
                continue
            if allowed[field].type is datetime:
                new_values = set()
                for val in value:
                    new_values.add(cast_datetime(val))
                value = new_values
            column = getattr(table.c, field)
            if op in OPERATORS:
                for val in value:
                    expr = OPERATORS[op](column, val)
                    complex_expressions.append(expr)
        else:
            if not key in allowed.keys():
                continue
            simple_kwargs[key] = value[0]

    if simple_kwargs:
        query = query.filter_by(**simple_kwargs)

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

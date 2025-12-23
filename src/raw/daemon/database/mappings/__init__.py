from sqlalchemy import Engine, Table

from ..metadata import metadata
from .entity import entities_table, links_table
from .folder import folders_table
from .note import notes_table
from .session import sessions_table
from .tag import tags_table
from .task import tasks_table
from ...entities import (
    Entity, Folder, Session, Tag, Task, Note
)


TABLES = {
    "links": links_table,
    "folders": folders_table,
    "notes": notes_table,
    "sessions": sessions_table,
    "tags": tags_table,
    "tasks": tasks_table,
    "entities": entities_table,
}

TABLES_COLUMNS = {
    table_name: table.c
    for table_name, table in TABLES.items()
}

TABLES_COLUMNS_NAMES = {
    table_name: columns.keys()
    for table_name, columns in TABLES_COLUMNS.items()
}

COLUMN_TO_TABLE_NAME = {
    column: table
    for table, columns in TABLES_COLUMNS_NAMES.items()
    for column in columns
}

COLUMN_TO_TABLE = {
    column: TABLES[table_name]
    for column, table_name in COLUMN_TO_TABLE_NAME.items()
}

TABLE_TO_ENTITY: dict[Table, type[Entity]] = {
    entities_table: Entity,
    folders_table: Folder, 
    sessions_table: Session,
    tags_table: Tag,
    tasks_table: Task,
    notes_table: Note,
}


def map_tables(engine: Engine):
    metadata.create_all(
        engine,
        tables=[t for t in TABLES.values()]
    )

from sqlalchemy import Engine, Table

from ..metadata import metadata
from .entity import entity_table, link_table
from .folder import folder_table
from .note import note_table
from .session import session_table
from .tag import tag_table
from .task import task_table
from ...entities import (
    Entity, Folder, Session, Tag, Task, Note
)


TABLES = {
    "link": link_table,
    "folder": folder_table,
    "note": note_table,
    "session": session_table,
    "tag": tag_table,
    "task": task_table,
    "entity": entity_table,
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
    entity_table: Entity,
    folder_table: Folder, 
    session_table: Session,
    tag_table: Tag,
    task_table: Task,
    note_table: Note,
}


def map_tables(engine: Engine):
    metadata.create_all(
        engine,
        tables=[t for t in TABLES.values()]
    )

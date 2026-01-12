from sqlalchemy import Engine

from ..metadata import metadata
from .entity import entity_table
from .task import task_table


TABLES = {
    "task": task_table,
    "entity": entity_table,
}


def create_tables(engine: Engine):
    metadata.create_all(
        engine,
        tables=[t for t in TABLES.values()]
    )

from sqlite3 import Connection

from .entity import entity_table
from .task import task_table


def create_tables(conn: Connection):
    c = conn.cursor()
    with conn:
        c.execute(entity_table)
        c.execute(task_table)

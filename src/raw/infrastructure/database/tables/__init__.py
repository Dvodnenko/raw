from sqlite3 import Connection

from .identity import identity_table
from .task import task_table


def create_tables(conn: Connection):
    c = conn.cursor()
    with conn:
        c.execute(identity_table)
        c.execute(task_table)

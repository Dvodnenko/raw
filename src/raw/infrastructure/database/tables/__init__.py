from sqlite3 import Connection
from pathlib import Path

from .identity import identity_table
from .task import task_table
from .note import note_table
from .session import session_table
from .folder import folder_table


def create_db_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()


def create_tables(conn: Connection):
    c = conn.cursor()
    
    with conn:
        c.execute(identity_table)
        c.execute(task_table)
        c.execute(note_table)
        c.execute(session_table)
        c.execute(folder_table)

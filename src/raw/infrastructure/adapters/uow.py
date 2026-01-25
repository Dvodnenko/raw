from typing import Optional
import sqlite3

from ...domain import UnitOfWork
from .repositories.task import TaskRepositorySQL
from .repositories.resolver import EntityTypeResolverSQL


class UnitOfWorkSQL(UnitOfWork):

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def __enter__(self):
        self._conn = sqlite3.connect(self._db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.execute("BEGIN")

        self.resolver = EntityTypeResolverSQL(self._conn)
        self.tasks = TaskRepositorySQL(self._conn)

        return self

    def __exit__(self, exc_type, *_):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self._conn.close()

    def commit(self):
        self._conn.execute("COMMIT")

    def rollback(self):
        self._conn.execute("ROLLBACK")

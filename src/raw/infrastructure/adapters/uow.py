from sqlalchemy import Connection

from ...domain import UnitOfWork
from .repository import TaskRepositorySA


class UnitOfWorkSA(UnitOfWork):

    def __init__(self, conn: Connection):
        self._conn = conn
        self._tx = None
        
        self.tasks = TaskRepositorySA(conn)

    def __enter__(self):
        if self._tx:
            raise RuntimeError("Transaction is already started")
        self._tx = self._conn.begin()
        return self
    
    def __exit__(self, exc_type, *_):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self):
        if self._tx is None:
            raise RuntimeError("Unit of work is not started")
        self._tx.commit()
        self._tx = None

    def rollback(self):
        if self._tx:
            self._tx.rollback()
            self._tx = None

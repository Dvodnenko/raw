from typing import Any

from sqlalchemy import Connection

from ..domain import Entity
from .dml import create, edit, delete
from .queries import filter
from .exc import handle_database_exceptions


class Repository:

    def __init__(self, conn: Connection):
        self.conn = conn

    # DMLs

    @handle_database_exceptions
    def create(self, obj: Entity):
        return create(self.conn, obj)
    
    def edit(self, id: int, **kwargs):
        return edit(self.conn, id, **kwargs)
    
    def delete(self, id: int):
        return delete(self.conn, id)
    
    # Queries

    def filter(
        self,
        filters: dict[str, tuple[Any]],
        batch_size: int
    ):
        yield from filter(self.conn, filters, batch_size)

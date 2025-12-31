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
    
    @handle_database_exceptions
    def edit(self, id: int = None, title: str = None, **kwargs):
        return edit(self.conn, id=id, title=title, **kwargs)
    
    @handle_database_exceptions
    def delete(self, id: int = None, title: str = None):
        return delete(self.conn, id=id, title=title)
    
    # Queries

    def filter(
        self,
        filters: dict[str, list[Any]],
    ):
        yield from filter(self.conn, filters)

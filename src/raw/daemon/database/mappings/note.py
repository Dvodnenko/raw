from sqlalchemy import Table, Column, Integer, ForeignKey, Text

from ..orm_registry import mapping_registry


notes_table = Table(
    "notes",
    mapping_registry.metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
           primary_key=True, autoincrement=True),
    Column("content", Text, nullable=False)
)

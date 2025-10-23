from sqlalchemy import Table, Column, Integer, ForeignKey

from ..orm_registry import mapping_registry


tags_table = Table(
    "tags",
    mapping_registry.metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
           primary_key=True, autoincrement=True),
)

from sqlalchemy import (
    Table, Column, Integer, Text, String, ForeignKey)

from ..metadata import metadata


entity_table = Table(
    "entity", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", String(50)),
    Column("parent_id", Integer, 
        ForeignKey("entity.id", ondelete="CASCADE"), nullable=True),
    Column("title", String, nullable=False, unique=True),
    Column("description", Text, nullable=True),
    Column("icon", String, nullable=False, default=""),
)

from sqlalchemy import (
    Table, Column, Integer, Text, String, ForeignKey, UniqueConstraint)

from ..metadata import metadata


entities_table = Table(
    "entities", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", String(50)),
    Column("parent_id", Integer, 
        ForeignKey("entities.id", ondelete="CASCADE"), nullable=True),
    Column("title", String, nullable=False),
    Column("description", Text, nullable=True),
    Column("styles", String),
    Column("icon", String, nullable=False, default=""),
    
    UniqueConstraint("title", name="uq_entities_title_type"),
)

links_table = Table(
    "links", metadata,
    Column("from_id", Integer, 
        ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True),
    Column("to_id", Integer, 
        ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True),

    UniqueConstraint("from_id", "to_id"),
)

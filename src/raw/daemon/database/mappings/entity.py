from sqlalchemy import (Table, Column, Integer, Text,
                        String, ForeignKey, UniqueConstraint)

from ..orm_registry import mapping_registry


entities_table = Table(
    "entities", mapping_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", String(50)),
    Column("parent_id", Integer, 
           ForeignKey("folders.id", ondelete="CASCADE"), nullable=True),
    Column("title", String, nullable=False),
    Column("description", Text, nullable=True),
    Column("styles", String),
    Column("icon", String, nullable=False, default=""),
    UniqueConstraint("title", "type", name="uq_entities_title_type"),
)

entity_links_table = Table(
    "entity_links", mapping_registry.metadata,
    Column("entity_id", Integer, 
           ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True),
    Column("link_id", Integer, 
           ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True),
)

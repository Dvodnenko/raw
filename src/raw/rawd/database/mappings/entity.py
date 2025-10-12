from sqlalchemy import (Table, Column, Integer, 
                        String, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship

from ...entities import Entity
from ..orm_registry import mapping_registry


entities_table = Table(
    "entities", mapping_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", String(50)),
    Column("parent_id", Integer, 
           ForeignKey("entities.id", ondelete="CASCADE"), nullable=True),
    Column("title", String, nullable=False),
    UniqueConstraint("title", "type", name="uq_entities_title_type"),
)

entity_refs_table = Table(
    "entity_refs", mapping_registry.metadata,
    Column("entity_id", Integer, 
           ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True),
    Column("ref_id", Integer, 
           ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True),
)

def map_entities_table():
    mapping_registry.map_imperatively(
        Entity,
        entities_table,
        polymorphic_on=entities_table.c.type,
        polymorphic_identity="entity",
        properties={
            "refs": relationship(
                "Entity",
                secondary=entity_refs_table,
                primaryjoin=entities_table.c.id == entity_refs_table.c.entity_id,
                secondaryjoin=entities_table.c.id == entity_refs_table.c.ref_id,
                lazy="joined",
            ),
            "parent": relationship(
                "Entity",
                remote_side=entities_table.c.id,
                backref="children"
            )
        }
    )

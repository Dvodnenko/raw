from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship


from ....domain import Entity
from ..orm_registry import mapping_registry


entities = Table(
    "entities", mapping_registry.metadata,
    Column("title", Integer, primary_key=True),
    Column("type", String),
)

links = Table(
    "links", mapping_registry.metadata,
    Column("title", Integer, primary_key=True),
    Column("source_title", ForeignKey("entities.title")),
    Column("target_title", ForeignKey("entities.title")),
)

def map_entities_table():
    mapping_registry.map_imperatively(
        Entity, entities,
        polymorphic_on=entities.c.type,
        polymorphic_identity="entity",
        properties={
            "refs": relationship(
                "Entity",
                secondary=links,
                primaryjoin=entities.c.title == links.c.source_title,
                secondaryjoin=entities.c.title == links.c.target_title,
                backref="backrefs"
            )
        }
    )

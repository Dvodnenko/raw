from sqlalchemy import Table, Column, Integer, ForeignKey, String, Enum

from ...entities import Folder, Entity, Color
from ..orm_registry import mapping_registry


folders_table = Table(
    "folders",
    mapping_registry.metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
           primary_key=True, autoincrement=True),
    Column("color", 
           Enum(Color, name="color_enum", create_type=True),
           nullable=False, default=Color.WHITE
    ),
    Column("icon", String, nullable=False, default="")
)


def map_folders_table():
    mapping_registry.map_imperatively(
        Folder, folders_table, inherits=Entity, 
        polymorphic_identity="folder",
    )

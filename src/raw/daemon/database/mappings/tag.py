from sqlalchemy import Table, Column, Integer, ForeignKey

from ..metadata import metadata


tags_table = Table(
    "tags", metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
        primary_key=True, autoincrement=True),
)

from sqlalchemy import Table, Column, Integer, ForeignKey

from ..metadata import metadata


folders_table = Table(
    "folders", metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
        primary_key=True, autoincrement=True),
)

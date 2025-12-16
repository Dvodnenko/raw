from sqlalchemy import Table, Column, Integer, ForeignKey, Text

from ..metadata import metadata


notes_table = Table(
    "notes", metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
        primary_key=True, autoincrement=True),
    Column("content", Text, nullable=False)
)

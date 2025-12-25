from sqlalchemy import Table, Column, Integer, ForeignKey, Text

from ..metadata import metadata


notes_table = Table(
    "notes", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
    Column("content", Text, nullable=False)
)

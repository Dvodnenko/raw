from sqlalchemy import Table, Column, Integer, ForeignKey, Text

from ..metadata import metadata


note_table = Table(
    "note", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entity.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
    Column("content", Text, nullable=False)
)

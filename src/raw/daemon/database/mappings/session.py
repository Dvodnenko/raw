from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, Text

from ..metadata import metadata


sessions_table = Table(
    "sessions", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
    Column("start", DateTime, nullable=False),
    Column("end", DateTime, nullable=True),
    Column("summary", Text, nullable=True),
)

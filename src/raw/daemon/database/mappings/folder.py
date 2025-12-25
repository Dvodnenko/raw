from sqlalchemy import Table, Column, Integer, ForeignKey

from ..metadata import metadata


folders_table = Table(
    "folders", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
)

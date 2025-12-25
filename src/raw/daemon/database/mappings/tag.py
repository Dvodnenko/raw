from sqlalchemy import Table, Column, Integer, ForeignKey

from ..metadata import metadata


tags_table = Table(
    "tags", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
)

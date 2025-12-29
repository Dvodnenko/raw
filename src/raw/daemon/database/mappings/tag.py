from sqlalchemy import Table, Column, Integer, ForeignKey

from ..metadata import metadata


tag_table = Table(
    "tag", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entity.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
)

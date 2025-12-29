from sqlalchemy import Table, Column, Integer, ForeignKey

from ..metadata import metadata


folder_table = Table(
    "folder", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entity.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
)

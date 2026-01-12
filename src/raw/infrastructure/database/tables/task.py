from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, Enum

from ....domain import TaskStatus
from ..metadata import metadata


task_table = Table(
    "task", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entity.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
    Column("deadline", DateTime, nullable=True),
    Column("status", 
       Enum(TaskStatus, name="task_status_enum", create_type=True),
       nullable=False, default=TaskStatus.ACTIVE
    ),
)
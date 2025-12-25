from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, Enum

from ..metadata import metadata
from .enums import TaskStatus


tasks_table = Table(
    "tasks", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    ),
    Column("deadline", DateTime, nullable=True),
    Column("status", 
       Enum(TaskStatus, name="task_status_enum", create_type=True),
       nullable=False, default=TaskStatus.INACTIVE
    ),
)

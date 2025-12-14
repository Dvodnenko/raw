from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, Enum

from ..orm_registry import mapping_registry
from ...entities import TaskStatus


tasks_table = Table(
    "tasks",
    mapping_registry.metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
           primary_key=True, autoincrement=True),
    Column("deadline", DateTime, nullable=True),
    Column("status", 
           Enum(TaskStatus, name="task_status_enum", create_type=True),
           nullable=False, default=TaskStatus.INACTIVE
    ),
)

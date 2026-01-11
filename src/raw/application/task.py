from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..domain import TaskStatus, TaskEditor


@dataclass(frozen=True)
class TaskView:
    id: int
    title: str
    description: str
    icon: str
    parent_id: Optional[int]
    status: TaskStatus
    deadline: Optional[datetime]

@dataclass(frozen=True)
class AddTaskCommand:
    title: str
    description: str = ""
    icon: str = ""
    status: TaskStatus = TaskStatus.ACTIVE
    deadline: datetime = None

@dataclass(frozen=True)
class EditTaskCommand:
    id: int
    editor: TaskEditor

@dataclass(frozen=True)
class RemoveTaskCommand:
    id: int

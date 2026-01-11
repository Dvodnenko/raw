from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..domain import TaskStatus, TaskEditor, UnitOfWork


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


class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def _extract_parent_title(self, full_path: str) -> Optional[str]:
        if full_path.count("/") == 1: # root entity
            return None
        return full_path[0:full_path.rfind("/")]

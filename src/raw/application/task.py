from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Iterator

from ..domain import Task, TaskStatus, Spec, TaskEditor, UnitOfWork


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
    
    def add(self, cmd: AddTaskCommand):
        obj = Task(
            # repository will generate the id by itself 
            # and we don't really need it here
            id=None,
            title=cmd.title,
            description=cmd.description,
            icon=cmd.icon,
            status=cmd.status,
            deadline=cmd.deadline,
        )

        parent_path: Optional[str] = self._extract_parent_path(cmd.title)

        with self.uow:
            if parent_path:
                parent = self.uow.tasks.get_by_title(parent_path)
                if not parent:
                    raise ValueError(
                        f"Cannot locate Task in {parent_path}/ because it does not exist"
                    )
                obj.parent_id = parent.id

            self.uow.tasks.add(obj)

    def filter(self, spec: Spec = None) -> Iterator[Task]:
        for task in self.uow.tasks.filter(spec):
            yield TaskView(
                id=task.id,
                title=task.title,
                description=task.description,
                icon=task.icon,
                parent_id=task.parent_id,
                status=task.status,
                deadline=task.deadline,
            )
    
    def edit(self, cmd: EditTaskCommand):
        with self.uow:
            task = self.uow.tasks.get_by_id(cmd.id)
            if not task:
                raise ValueError("Such Task does not exist")
            old_title = task.title
            edited = cmd.editor.apply(task)
            self.uow.tasks.save(edited)
            if old_title != edited.title:
                self.uow.tasks.rewrite_subtree_titles(
                    old_prefix=old_title,
                    new_prefix=edited.title,
                )

    def _extract_parent_title(self, full_path: str) -> Optional[str]:
        if full_path.count("/") == 1: # root entity
            return None
        return full_path[0:full_path.rfind("/")]

from dataclasses import dataclass
from typing import Optional, Any

from ...domain import (
    UnitOfWork, TaskEditor, NotFound,
    InvalidState, EntityRef, EntityType
)
from ..common import _extract_parent_title
from ...shared import MISSING


@dataclass(frozen=True)
class EditTaskCmd:
    id: int
    editor: TaskEditor

class EditTask:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def edit(self, cmd: EditTaskCmd):
        with self.uow:
            task = self.uow.tasks.get_by_id(cmd.id)
            if not task:
                raise NotFound(EntityRef(EntityType.TASK, cmd.id))
            if cmd.editor.title is not MISSING: # user tries to edit the title
                if cmd.editor.title.startswith(task.title+"/"): # ! user tries to move task into itself
                    raise InvalidState("cannot move task into itself")
            old_title = task.title
            old_parent_path: Optional[str] = _extract_parent_title(task.title)
            new_parent_path: Optional[str] = _extract_parent_title(cmd.editor.title)
            new_parent_id: Optional[int] = None
            if old_parent_path != new_parent_path:
                # checking if the new parent exists
                new_parent = self.uow.tasks.get_by_title(new_parent_path)
                if not new_parent:
                    raise NotFound(EntityRef(EntityType.TASK, new_parent_path))
                new_parent_id = new_parent.id
            edited = cmd.editor.apply(task)
            if new_parent_id:
                edited.parent_id = new_parent_id
            self.uow.tasks.save(edited)
            if old_title != edited.title:
                self.uow.tasks.rewrite_subtree_titles(
                    old_prefix=old_title,
                    new_prefix=edited.title,
                )


@dataclass(frozen=True)
class EditEntityCmd:
    id: int
    fields: dict[str, Any]

class EditEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def edit(self, cmd: EditEntityCmd):
        with self.uow:
            type = self.uow.resolver.resolve(cmd.id)
        
        if type is EntityType.TASK:
            cmd = EditTaskCmd(
                cmd.id,
                TaskEditor(**cmd.fields)
            )
            EditTask(self.uow).edit(cmd)


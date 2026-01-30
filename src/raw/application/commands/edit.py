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
            # 1. check if the task even exists
            task = self.uow.tasks.get_by_id(cmd.id)
            if not task:
                raise NotFound(EntityRef(EntityType.TASK, cmd.id))
            
            # 2. remember his old title and parent's old title, in case user edits it
            old_title = task.title
            old_parent_path: Optional[str] = _extract_parent_title(old_title)

            # 3. register optional value of new parent, if it is edited also
            new_parent_path: Optional[str] = None

            if cmd.editor.title is not MISSING: # user tries to edit the title
                if cmd.editor.title.startswith(task.title+"/"): # ! user tries to move task into itself
                    raise InvalidState("cannot move task into itself")
            # check if user changed parent
            # or only title of task itself (only title = last title segment,
            # in "/a/b/c" it's "c")
            edited = cmd.editor.apply(task)
            if _extract_parent_title(edited.title) != old_parent_path: # parent changed
                # checking if the new parent exists
                new_parent = self.uow.tasks.get_by_title(new_parent_path)
                if not new_parent:
                    raise NotFound(EntityRef(EntityType.TASK, new_parent_path))
                # parent id changes ONLY if:
                # 1. parent title was changed
                # 2. new parent exists
                edited.parent_id = new_parent.id

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


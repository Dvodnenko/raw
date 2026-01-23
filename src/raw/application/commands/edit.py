from dataclasses import dataclass
from typing import Optional

from ...domain import UnitOfWork, TaskEditor
from ..common import _extract_parent_title


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
                raise ValueError("Such Task does not exist")
            old_title = task.title
            old_parent_path: Optional[str] = _extract_parent_title(task.title)
            new_parent_path: Optional[str] = _extract_parent_title(cmd.editor.title)
            if old_parent_path != new_parent_path:
                # checking if the new parent exists
                new_parent = self.uow.tasks.get_by_title(new_parent_path)
                if not new_parent:
                    raise ValueError(f"Parent not found: {new_parent_path}")
                cmd.editor.parent_id = new_parent.id
            edited = cmd.editor.apply(task)
            self.uow.tasks.save(edited)
            if old_title != edited.title:
                self.uow.tasks.rewrite_subtree_titles(
                    old_prefix=old_title,
                    new_prefix=edited.title,
                )

from dataclasses import dataclass

from ...domain import UnitOfWork, TaskEditor


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
            edited = cmd.editor.apply(task)
            self.uow.tasks.save(edited)
            if old_title != edited.title:
                self.uow.tasks.rewrite_subtree_titles(
                    old_prefix=old_title,
                    new_prefix=edited.title,
                )

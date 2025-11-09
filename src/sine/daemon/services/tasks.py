from ..repositories.task import saTaskRepository
from ..repositories.folder import saFolderRepository
from ..entities import Task
from ..database.funcs import get_all_by_titles
from .decorators import provide_conf, cast_kwargs


class TaskService:
    def __init__(self, repository: saTaskRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)

    @cast_kwargs(Task)
    def create(self, args: list, flags: list, **kwargs):
        task = Task(**kwargs)
        if next(self.repository.get(task.title)):
            yield f"Task already exists: {task.title}", 1
            return
        next(self.repository.create(task))
        yield f"Task created: {task.title}", 0
    
    @provide_conf
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "title")
        if "t" in flags:
            for task in self.repository.get_all(sortby):
                yield task.title, 0
        else:
            pattern: str = kwargs["__cnf"]["formats"]["task"]
            for task in self.repository.get_all(sortby):
                yield pattern.format(**task.to_dict()), 0
    
    @provide_conf
    def print(self, args: list, flags: list, **kwargs):
        pattern: str = kwargs["__cnf"]["formats"]["task"]
        for task in get_all_by_titles(self.repository.session, Task, args):
            yield pattern.format(**task.to_dict()), 0
    
    @cast_kwargs(Task)
    def update(self, args: list, flags: list, **kwargs):
        current = next(self.repository.get(args[0]))
        if not current:
            yield f"Task not found: {args[0]}", 1
            return
        next(self.repository.update(args[0], **kwargs))
        yield f"Task updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        task = next(self.repository.get(args[0]))
        if not task:
            yield f"Task not found: {args[0]}", 1
            return
        next(self.repository.delete(task))
        yield f"Task deleted: {args[0]}", 0

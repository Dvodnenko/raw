from ..repositories.folder import saFolderRepository
from ..entities import Folder
from ..database.funcs import get_all_by_titles
from .decorators import provide_conf, cast_kwargs


class FolderService:
    def __init__(self, repository: saFolderRepository):
        self.repository = repository

    @cast_kwargs(Folder)
    def create(self, args: list, flags: list, **kwargs) -> tuple[str, int]:
        folder = Folder(**kwargs)
        if self.repository.get(folder.title):
            return f"Folder already exists: {folder.title}", 1
        self.repository.create(folder)
        return f"Folder created: {folder.title}", 0
    
    @provide_conf
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "title")
        folders = self.repository.get_all()
        folders = sorted(
            folders,
            key=lambda f: getattr(f, sortby),
            reverse="r" in flags
        )
        pattern: str = kwargs["__cnf"]["formats"]["folder"]
        if "t" in flags:
            return "".join(f"{f.title}\n" for f in folders)[:-1], 0
        return "".join([f"{pattern.format(
            **f.to_dict())}" for f in folders]).rstrip(), 0
    
    @provide_conf
    def print(self, args: list, flags: list, **kwargs):
        folders = get_all_by_titles(self.repository.session, Folder, args)
        pattern: str = kwargs["__cnf"]["formats"]["folder"]
        return "".join([f"{pattern.format(
            **f.to_dict())}" for f in folders]).rstrip(), 0
    
    @cast_kwargs(Folder)
    def update(self, args: list, flags: list, **kwargs):
        current = self.repository.get(args[0])
        if not current:
            return f"Folder not found: {args[0]}", 1
        self.repository.update(args[0], **kwargs)
        return f"Folder updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        folder = self.repository.get(args[0])
        delete = False
        if not folder:
            return f"Folder not found: {args[0]}", 1
        if folder.children:
            if "F" in flags:
                delete = True
        else: delete = True
        if delete:
            self.repository.delete(folder)
            return f"Folder deleted: {args[0]}", 0
        else:
            return (f"cannot delete Folder '{args[0]}' because it is not empty"), 1

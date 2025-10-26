from ..repositories.tag import saTagRepository
from ..repositories.folder import saFolderRepository
from ..entities import Tag, Entity
from ..database.funcs import get_all_by_titles
from ..decorators import provide_conf


class TagService:
    def __init__(self, repository: saTagRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)

    def cast_kwargs(self, **kwargs):
        _tcm = {
            "color": lambda x: int(x),
            "links": lambda x: get_all_by_titles(Entity, x.split(",")),
        }
        keys = set(_tcm.keys()).intersection(kwargs.keys())
        for key in keys:
            kwargs[key] = _tcm[key](kwargs[key])
        return kwargs

    def create(self, args: list, flags: list, **kwargs) -> tuple[str, int]:
        tag = Tag(**self.cast_kwargs(**kwargs))
        if self.repository.get(tag.title):
            return f"Tag already exists: {tag.title}", 1
        if tag.parentstr != "":
            if not self.folders_repository.get(tag.parentstr):
                return f"Tag not found: {tag.parentstr}", 1
        self.repository.create(tag)
        return f"Tag created: {tag.title}", 0
    
    @provide_conf
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "title")
        tags = self.repository.get_all()
        tags = sorted(
            tags,
            key=lambda t: getattr(t, sortby),
            reverse="r" in flags
        )
        pattern: str = kwargs["__cnf"]["formats"]["tag"]
        if "t" in flags:
            return "".join(f"{t.title}\n" for t in tags)[:-1], 0
        return "".join([f"{pattern.format(
            **t.to_dict())}" for t in tags]).rstrip(), 0
    
    @provide_conf
    def print(self, args: list, flags: list, **kwargs):
        tags = get_all_by_titles(self.repository.session, Tag, args)
        pattern: str = kwargs["__cnf"]["formats"]["tag"]
        return "".join([f"{pattern.format(
            **t.to_dict())}" for t in tags]).rstrip(), 0
        
    def update(self, args: list, flags: list, **kwargs):
        kwargs = self.cast_kwargs(**kwargs)
        current = self.repository.get(args[0])
        if not current:
            return f"Tag not found: {args[0]}", 1
        self.repository.update(args[0], **kwargs)
        return f"Tag updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        tag = self.repository.get(args[0])
        if not tag:
            return f"Tag not found: {args[0]}", 1
        self.repository.delete(tag)
        return f"Tag deleted: {args[0]}", 0

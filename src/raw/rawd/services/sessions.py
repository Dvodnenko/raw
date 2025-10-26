from datetime import datetime

from ..repositories.session import saSessionRepository
from ..repositories.folder import saFolderRepository
from ..entities import Session
from ..database.funcs import get_all_by_titles
from .decorators import provide_conf, cast_kwargs


class SessionService:
    def __init__(self, repository: saSessionRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)
        self.active: Session | None = None

    @cast_kwargs(Session)
    def begin(self, args: list, flags: list, **kwargs) -> tuple[str, int]:
        print(f"kwargs: {kwargs}")
        active = self.get_active()
        if active:
            return f"Session is already started: '{active.title}'", 1
        kwargs["start"] = kwargs.get("start") or \
            datetime.now().replace(microsecond=0)
        session = Session(**kwargs)
        print(f"Session: {session}")
        self.repository.create(session)
        return f"Session started", 0
    
    @cast_kwargs(Session)
    def stop(self, args: list, flags: list, **kwargs):
        session = self.get_active()
        if not session:
            return "Active Session not found", 1
        kwargs["end"] = kwargs.get("end") or \
            datetime.now().replace(microsecond=0)
        self.repository.update(session.title, **kwargs)
        return "Session stoped", 0
    
    def get_active(self):
        if self.active:
            return self.active
        return self.repository.get_active()
    
    @provide_conf
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "start")
        sessions = self.repository.get_all()
        sessions = sorted(
            sessions,
            key=lambda f: getattr(f, sortby),
            reverse="r" in flags
        )
        if "t" in flags:
            return "".join(f"{s.title}\n" for s in sessions)[:-1], 0
        pattern: str = kwargs["__cnf"]["formats"]["session"]
        return "".join([f"{pattern.format(
            **s.to_dict()).rstrip()}\n" for s in sessions]).rstrip(), 0
    
    @provide_conf
    def print(self, args: list, flags: list, **kwargs):
        sessions = get_all_by_titles(self.repository.session, Session, args)
        pattern: str = kwargs["__cnf"]["formats"]["session"]
        return "".join([f"{pattern.format(
            **s.to_dict()).rstrip()}\n" for s in sessions]).rstrip(), 0
    
    @cast_kwargs(Session)
    def update(self, args: list, flags: list, **kwargs):
        current = self.repository.get(args[0])
        if not current:
            return f"Session not found: {args[0]}", 1
        self.repository.update(args[0], **kwargs)
        return f"Session updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        session = self.repository.get(args[0])
        if not session:
            return f"Session not found: {args[0]}", 1
        self.repository.delete(session)
        return f"Session deleted: {args[0]}", 0

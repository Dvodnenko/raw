from datetime import datetime

from sqlalchemy import select

from ..repositories.session import saSessionRepository
from ..repositories.folder import saFolderRepository
from ..entities import Session, Entity
from ..database.session import Session as ormSession
from ..database.funcs import get_all_by_titles
from ..decorators import provide_conf


class SessionService:
    def __init__(self):
        self.repository = saSessionRepository(ormSession())
        self.folders_repository = saFolderRepository(ormSession())
        self.active: Session | None = None

    def begin(self, args: list, flags: list, **kwargs) -> tuple[str, int]:
        active = self.get_active()
        if active:
            return f"Session is already started: '{active.title}'", 1
        refs = kwargs.get("refs")
        if refs:
            refs_list = refs.split(",")
            query = select(Entity).where(Entity.title.in_(refs_list))
            entities = self.repository.session.scalars(query).unique().all()
            kwargs["refs"] = entities
        if kwargs.get("start"):
            kwargs["start"] = datetime.fromisoformat(kwargs.get("start")).replace(microsecond=0)
        else:
            kwargs["start"] = datetime.now().replace(microsecond=0)
        if kwargs.get("color"):
            kwargs["color"] = int(kwargs["color"])
        session = Session(**kwargs)
        if session.parentstr != "":
            if not self.folders_repository.get(session.parentstr):
                return f"Folder not found: {session.parentstr}", 1
        self.repository.create(session)
        return f"Session started", 0
    
    def stop(self, args: list, flags: list, **kwargs):
        session = self.get_active()
        if not session:
            return "Active Session not found", 1
        refs = kwargs.get("refs")
        if refs:
            refs_list = refs.split(",")
            query = select(Entity).where(Entity.title.in_(refs_list))
            entities = self.repository.session.scalars(query).unique().all()
            kwargs["refs"] = entities
        if kwargs.get("end"):
            kwargs["end"] = datetime.fromisoformat(kwargs.get("end")).replace(microsecond=0)
        else:
            kwargs["end"] = datetime.now().replace(microsecond=0)
        if kwargs.get("color"):
            kwargs["color"] = int(kwargs["color"])
        kwargs["end"].replace(microsecond=0)
        current_title = session.title
        self.repository.update(current_title, **kwargs)
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
        
    def update(self, args: list, flags: list, **kwargs):
        refs = kwargs.get("refs")
        if "refs" in kwargs.keys():
            if refs is "":
                kwargs["refs"] = []
            else:
                refs_list = refs.split(",")
                query = select(Entity).where(Entity.title.in_(refs_list))
                entities = self.repository.session.scalars(query).unique().all()
                kwargs["refs"] = entities
        if kwargs.get("color"):
            kwargs["color"] = int(kwargs["color"])
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

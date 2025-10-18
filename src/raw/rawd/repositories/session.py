from sqlalchemy import select
from sqlalchemy.orm import Session as ormSession

from ..entities import Session


class saSessionRepository:
    def __init__(self, session: ormSession):
        self.session = session

    def create(self, session: Session) -> None:
        if session.parentstr != "":
            parent = self.get(session.parentstr)
            session.parent = parent
        self.session.add(session)
        self.session.commit()
        return None

    def get(self, title: str) -> Session | None:
        query = select(Session) \
            .where(Session.title == title)
        obj = self.session.scalars(query).first()
        return obj
    
    def get_active(self):
        query = select(Session) \
            .where(Session.end == None)
        obj = self.session.scalars(query).first()
        return obj

    def get_all(self) -> list[Session]:
        query = select(Session)
        sessions = self.session.scalars(query).unique().all()
        return sessions

    def update(self, title_: str, **kwargs) -> None:
        session = (self.session.query(Session)
                  .filter_by(title=title_)
                  .first())
        session = session.update(**kwargs)
        self.session.commit()
        return None

    def delete(self, entity: Session) -> None:
        self.session.delete(entity)
        self.session.commit()
        return None

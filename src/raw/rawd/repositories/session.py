from sqlalchemy import select, update
from sqlalchemy.orm import Session as ormSession
from ..database.session import transaction

from ..entities import Session


class saSessionRepository:
    def __init__(self, session: ormSession):
        self.session = session

    @transaction
    def create(self, session: Session) -> None:
        self.session.add(session)
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

    @transaction
    def update(self, title_: str, **kwargs) -> None:
        session = (self.session.query(Session)
                  .filter_by(title=title_)
                  .first())
        session = session.update(**kwargs)
        self.session.merge(instance=session)
        return None

    @transaction
    def delete(self, entity: Session) -> None:
        self.session.delete(entity)
        return None

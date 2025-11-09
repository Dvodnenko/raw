from sqlalchemy import select
from sqlalchemy.orm import Session as ormSession

from ..entities import Session


class saSessionRepository:
    def __init__(self, session: ormSession):
        self.session = session

    def create(self, session: Session):
        self.session.add(session)
        self.session.commit()
        yield

    def get(self, title: str):
        query = select(Session) \
            .where(Session.title == title)
        obj = self.session.scalars(query).first()
        yield obj
    
    def get_active(self):
        query = select(Session) \
            .where(Session.end == None)
        obj = self.session.scalars(query).first()
        yield obj

    def get_all(self, order_by: str = "title"):
        batch_size = 100
        offset = 0
        while True:
            batch = self.session.query(Session).order_by(getattr(Session, order_by)).\
                limit(batch_size).offset(offset).all()
            if not batch:
                break
            for obj in batch:
                yield obj
            offset += batch_size

    def update(self, title_: str, **kwargs):
        session = (self.session.query(Session)
                  .filter_by(title=title_)
                  .first())
        session = session.update(**kwargs)
        self.session.merge(instance=session)
        self.session.commit()
        yield

    def delete(self, entity: Session):
        self.session.delete(entity)
        self.session.commit()
        yield

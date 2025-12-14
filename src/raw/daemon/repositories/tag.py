from sqlalchemy import select
from sqlalchemy.orm import Session as ormSession

from ..entities import Tag


class saTagRepository:
    def __init__(self, session: ormSession):
        self.session = session

    def create(self, tag: Tag):
        self.session.add(tag)
        self.session.commit()
        yield

    def get(self, title: str):
        query = select(Tag) \
            .where(Tag.title == title)
        obj = self.session.scalars(query).first()
        yield obj

    def get_all(self, order_by: str = "title"):
        batch_size = 100
        offset = 0
        while True:
            batch = self.session.query(Tag).order_by(getattr(Tag, order_by)).\
                limit(batch_size).offset(offset).all()
            if not batch:
                break
            for obj in batch:
                yield obj
            offset += batch_size

    def update(self, title_: str, **kwargs):
        tag = (self.session.query(Tag)
                  .filter_by(title=title_)
                  .first())
        tag = tag.update(**kwargs)
        self.session.commit()
        yield

    def delete(self, entity: Tag):
        self.session.delete(entity)
        self.session.commit()
        yield

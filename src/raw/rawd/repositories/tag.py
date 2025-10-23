from sqlalchemy import select
from sqlalchemy.orm import Session as ormSession

from ..entities import Tag


class saTagRepository:
    def __init__(self, session: ormSession):
        self.session = session

    def create(self, tag: Tag) -> None:
        if tag.parentstr != "":
            parent = self.get(tag.parentstr)
            tag.parent = parent
        self.session.add(tag)
        self.session.commit()
        return None

    def get(self, title: str) -> Tag | None:
        query = select(Tag) \
            .where(Tag.title == title)
        obj = self.session.scalars(query).first()
        return obj

    def get_all(self) -> list[Tag]:
        query = select(Tag)
        tags = self.session.scalars(query).unique().all()
        return tags

    def update(self, title_: str, **kwargs) -> None:
        tag = (self.session.query(Tag)
                  .filter_by(title=title_)
                  .first())
        tag = tag.update(**kwargs)
        self.session.commit()
        return None

    def delete(self, entity: Tag) -> None:
        self.session.delete(entity)
        self.session.commit()
        return None

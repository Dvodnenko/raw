from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..entities import Folder, Entity


class saFolderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, folder: Folder):
        self.session.add(folder)
        self.session.commit()
        yield

    def get(self, title: str):
        query = select(Folder) \
            .where(Folder.title == title)
        obj = self.session.scalars(query).first()
        yield obj

    def get_all(self, order_by: str = "title"):
        batch_size = 100
        offset = 0
        while True:
            batch = self.session.query(Folder).order_by(getattr(Folder, order_by)).\
                limit(batch_size).offset(offset).all()
            if not batch:
                break
            for obj in batch:
                yield obj
            offset += batch_size

    def update(self, title_: str, **kwargs):
        folder = (self.session.query(Folder)
                  .filter_by(title=title_)
                  .first())
        folder = folder.update(**kwargs)
        if folder.children:
            children = (self.session.query(Entity)
                        .where(Entity.title.like(f"{title_}/%"))
                        .all())
            for c in children:
                relative = Path(c.title).relative_to(title_)
                c.title = f"{folder.title}/{relative}"
        self.session.commit()
        yield

    def delete(self, entity: Folder):
        self.session.delete(entity)
        self.session.commit()
        yield

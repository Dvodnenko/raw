from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database.session import transaction

from ..entities import Folder, Entity


class saFolderRepository:
    def __init__(self, session: Session):
        self.session = session

    @transaction
    def create(self, folder: Folder) -> None:
        self.session.add(folder)
        return None

    def get(self, title: str) -> Folder | None:
        query = select(Folder) \
            .where(Folder.title == title)
        obj = self.session.scalars(query).first()
        return obj

    def get_all(self) -> list[Folder]:
        query = select(Folder)
        folders = self.session.scalars(query).unique().all()
        return folders

    @transaction
    def update(self, title_: str, **kwargs) -> None:
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
        return None

    @transaction
    def delete(self, entity: Folder) -> None:
        self.session.delete(entity)
        return None

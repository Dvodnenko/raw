from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..entities import Folder


class saFolderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, folder: Folder) -> None:
        if folder.title != "":
            folder.parent = self.get(folder.parentstr)
        self.session.add(folder)
        self.session.commit()
        return None

    def get(self, title: str) -> Folder | None:
        query = select(Folder) \
            .where(Folder.title == title)
        obj = self.session.scalars(query).first()
        return obj

    def get_all(self) -> list[Folder]:
        query = select(Folder)
        folders = self.session.scalars(query).all()
        return folders

    def update(self, title: str, new: Folder) -> None:
        if new.title != title:
            children = self.session.query(Folder).where(
                Folder.title.like(f"{title}/%")).all()
            for f in children:
                relative = Path(f.title).relative_to(title)
                f.title = f"{new.title}/{relative}"
        folder = self.session.query(Folder).where(Folder.title==title).first()
        folder.title,folder.refs,folder.color,folder.icon,folder.parent=(
            new.title,new.refs,new.color,new.icon,new.parent
        )
        self.session.commit()
        return None

    def delete(self, entity: Folder) -> None:
        self.session.delete(entity)
        return None
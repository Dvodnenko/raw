from dataclasses import dataclass
from typing import Optional, Iterator

from ....domain import UnitOfWork, Spec


@dataclass(frozen=True)
class FolderView:
    id: int
    title: str
    description: str
    icon: str
    parent_id: Optional[int]
    type: str = "folder"

@dataclass(frozen=True)
class FindFolderQuery:
    spec: Spec
    
    # Optionals
    order_by: str
    reverse: bool = False

class FindFolder:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find(self, query: FindFolderQuery) -> Iterator[FolderView]:
        with self.uow:
            for note in self.uow.folders.filter(
                query.spec,
                query.order_by,
                query.reverse,
            ):
                yield FolderView(
                    id=note.id,
                    title=note.title,
                    description=note.description,
                    icon=note.icon,
                    parent_id=note.parent_id,
                )

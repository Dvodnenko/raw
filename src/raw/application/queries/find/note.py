from dataclasses import dataclass
from typing import Optional, Iterator

from ....domain import UnitOfWork, Spec


@dataclass(frozen=True)
class NoteView:
    id: int
    title: str
    description: str
    icon: str
    parent_id: Optional[int]
    content: str
    type: str = "note"

@dataclass(frozen=True)
class FindNoteQuery:
    spec: Spec
    
    # Optionals
    order_by: str
    reverse: bool = False

class FindNote:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find(self, query: FindNoteQuery) -> Iterator[NoteView]:
        with self.uow:
            for note in self.uow.notes.filter(
                query.spec,
                query.order_by,
                query.reverse,
            ):
                yield NoteView(
                    id=note.id,
                    title=note.title,
                    description=note.description,
                    icon=note.icon,
                    parent_id=note.parent_id,
                    content=note.content,
                )

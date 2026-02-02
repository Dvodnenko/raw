from dataclasses import dataclass
from typing import Optional, Iterator
from datetime import datetime, timedelta

from ....domain import UnitOfWork, Spec


@dataclass(frozen=True)
class SessionView:
    id: int
    title: str
    description: str
    icon: str
    parent_id: Optional[int]
    message: str
    summary: str
    started_at: datetime
    ended_at: Optional[datetime]
    is_active: bool
    duration: timedelta
    type: str = "session"

@dataclass(frozen=True)
class FindSessionQuery:
    spec: Spec
    
    # Optionals
    order_by: str
    reverse: bool = False

class FindSession:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def find(self, query: FindSessionQuery) -> Iterator[SessionView]:
        with self.uow:
            for session in self.uow.sessions.filter(
                query.spec,
                query.order_by,
                query.reverse,
            ):
                yield SessionView(
                    id=session.id,
                    title=session.title,
                    description=session.description,
                    icon=session.icon,
                    parent_id=session.parent_id,
                    message=session.message,
                    summary=session.summary,
                    started_at=session.started_at,
                    ended_at=session.ended_at,
                    is_active=session.is_active,
                    duration=session.duration
                )

from dataclasses import dataclass
from typing import Iterator

from ...domain import UnitOfWork
from .find import SessionView


@dataclass(frozen=True)
class GetActiveSessionQuery:
    order_by: str
    reverse: bool = False

class GetActiveSessions:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_active_sessions(self, query: GetActiveSessionQuery) -> Iterator[SessionView]:
        with self.uow:
            for session in self.uow.sessions.get_active_sessions(
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

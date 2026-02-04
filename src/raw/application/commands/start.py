from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ...domain import (
    Session, UnitOfWork,
    NotFound, AlreadyExists, EntityRef
)
from ..common import _extract_parent_title


@dataclass(frozen=True)
class StartSessionCmd:
    title: Optional[str] = ""
    description: Optional[str] = ""
    icon: Optional[str] = ""
    message: Optional[str] = ""
    summary: Optional[str] = ""
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class StartSession:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def start(self, cmd: StartSessionCmd):
        obj = Session(
            # repository will generate the id by itself 
            # and we don't really need it here
            id=None,
            title=cmd.title,
            description=cmd.description,
            icon=cmd.icon,
            message=cmd.message,
            summary=cmd.summary,
            started_at=cmd.started_at or datetime.now().replace(microsecond=0),
            ended_at=cmd.ended_at,
        )

        parent_path: Optional[str] = _extract_parent_title(cmd.title)

        with self.uow:
            already_exists = self.uow.intertype.resolve_type_by_title(obj.title) is not None
            if already_exists:
                raise AlreadyExists(EntityRef(obj.title))

            if parent_path:
                parent_id = self.uow.intertype.resolve_id_by_title(parent_path)
                if not parent_id:
                    raise NotFound(EntityRef(parent_path))
                obj.parent_id = parent_id

            self.uow.sessions.add(obj)

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from hashlib import blake2b

from ..base.entity import Entity
from ..session.exceptions import SessionIsActiveError


def generate_title():
    return blake2b(digest_size=10).hexdigest()


@dataclass(kw_only=True, eq=False)
class Session(Entity):
    start: datetime
    title: str = field(default_factory=generate_title)
    summary: str | None = field(default=None, kw_only=True)
    end: datetime | None = field(default=None, kw_only=True)

    @property
    def is_active(self) -> bool:
        "Wether the Session is active"
        return self.end is None

    @property
    def total(self) -> timedelta:
        if self.is_active:
            raise SessionIsActiveError('Total time is not accessible because the session is still active')
        res = self.end - self.start
        return res

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from ..base.entity import Entity
from ..session.exceptions import SessionIsActiveError


@dataclass(kw_only=True, eq=False)
class Session(Entity):
    message: str | None = field(default=None)
    summary: str | None = field(default=None)
    start: datetime
    end: datetime | None = field(default=None)
    _breaks: list[timedelta] = field(default_factory=lambda : [])

    @property
    def is_active(self) -> bool:
        "Wether the Session is active"
        return self.end is None
    
    @property
    def breaks(self) -> timedelta:
        res = timedelta(0, 0, 0, 0, 0, 0, 0)
        for td in self._breaks:
            res += td
        return res

    @property
    def total(self) -> timedelta:
        if self.is_active:
            raise SessionIsActiveError('Total time is not accessible because the session is still active')
        res = self.end - self.start - self.breaks
        return res

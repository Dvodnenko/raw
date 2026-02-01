from dataclasses import dataclass
import re

from ..domain import InvalidValue


@dataclass(frozen=True)
class Identifier:

    value: str

    @property
    def is_id(self) -> bool:
        return self.value.isdigit()
    
    @property
    def is_title(self) -> bool:
        return (re.
            compile(r"^/(?:[A-Za-z0-9 _-]+)(?:/[A-Za-z0-9 _-]+)*$").
            match(self.value)) is not None

    def __post_init__(self):
        if (not self.is_id) and (not self.is_title):
            raise InvalidValue("invalid identifier")

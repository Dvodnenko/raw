from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FieldSpec:
    field: str
    operator: str
    value: Any

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FieldSpec:
    field: str
    operator: str
    value: Any


@dataclass(frozen=True)
class AndSpec:
    left: Any
    right: Any

@dataclass(frozen=True)
class OrSpec:
    left: Any
    right: Any

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FieldSpec:
    field: str
    operator: str
    value: Any


@dataclass(frozen=True)
class And:
    left: Any
    right: Any

@dataclass(frozen=True)
class Or:
    left: Any
    right: Any

@dataclass(frozen=True)
class Not:
    spec: Any

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Spec:
    ...


@dataclass(frozen=True)
class FieldSpec(Spec):
    field: str
    operator: str
    value: Any


@dataclass(frozen=True)
class And(Spec):
    left: Any
    right: Any

@dataclass(frozen=True)
class Or(Spec):
    left: Any
    right: Any

@dataclass(frozen=True)
class Not(Spec):
    spec: Any

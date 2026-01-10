from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Spec:
    ...


@dataclass(frozen=True)
class FieldSpec(Spec):
    field: str
    operator: str # NOTE: add Enum for this field
    value: Any


@dataclass(frozen=True)
class And(Spec):
    items: tuple[Spec]

@dataclass(frozen=True)
class Or(Spec):
    items: tuple[Spec]

@dataclass(frozen=True)
class Not(Spec):
    spec: Spec

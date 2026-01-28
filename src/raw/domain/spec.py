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
    left: Spec
    right: Spec

@dataclass(frozen=True)
class Or(Spec):
    left: Spec
    right: Spec

@dataclass(frozen=True)
class Not(Spec):
    spec: Spec


def and_(*clauses: Spec):
    return And(items=clauses)

def or_(*clauses: Spec):
    return Or(items=clauses)

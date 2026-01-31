from dataclasses import dataclass
from typing import Any
from enum import Enum


@dataclass(frozen=True)
class Spec:
    ...


class Operator(Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    LIKE = "like"
    IN = "in"


@dataclass(frozen=True)
class FieldSpec(Spec):
    field: str
    operator: Operator
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

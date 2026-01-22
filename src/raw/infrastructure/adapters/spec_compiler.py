from typing import Any
from datetime import datetime, date
from enum import Enum

from sqlglot import exp

from ...domain import FieldSpec, And, Or, Not, Spec


OPERATOR_MAP = {
    "eq": lambda f, v: f.eq(v),
    "ne": lambda f, v: f.neq(v),
    "gt": lambda f, v: f > v,
    "gte": lambda f, v: f >= v,
    "lt": lambda f, v: f < v,
    "lte": lambda f, v: f <= v,
    "like": lambda f, v: f.like(v),
    "in": lambda f, v: f.isin(v),
}


class SpecCompilerSQL:
    def compile(self, spec: Spec):
        match spec:
            case FieldSpec(field=field, operator=op, value=value):
                return self._compile_field(field, op, value)

            case And(items=items):
                return exp.and_(*[self.compile(s) for s in items])

            case Or(items=items):
                return exp.or_(*[self.compile(s) for s in items])

            case Not(spec=inner):
                return exp.not_(self.compile(inner))

            case _:
                raise TypeError(f"Unknown Spec type: {type(spec)}")

    def _compile_field(self, field: str, operator: str, value: Any) -> exp.Expression:
        if operator not in OPERATOR_MAP:
            raise ValueError(f"Unsupported operator: {operator}")

        column = exp.column(field)

        if operator == "in":
            if not isinstance(value, (list, tuple, set)):
                raise TypeError("IN operator expects iterable value")

            literals = [exp.Literal(this=v) for v in value]
            return column.isin(exp.Tuple(expressions=literals))

        literal = self._to_sql_literal(value)
        return OPERATOR_MAP[operator](column, literal)

    def _to_sql_literal(self, value: Any) -> exp.Expression:
        if value is None:
            return exp.Null()

        if isinstance(value, bool):
            return exp.Boolean(this=value)

        if isinstance(value, int):
            return exp.Literal.number(value)

        if isinstance(value, float):
            return exp.Literal.number(value)

        if isinstance(value, str):
            return exp.Literal.string(value)

        if isinstance(value, datetime):
            return exp.Literal.string(
                value.replace(microsecond=0).isoformat(sep=" ")
            )

        if isinstance(value, date):
            return exp.Literal.string(value.isoformat())

        if isinstance(value, Enum):
            return exp.Literal.string(value.value)

        if isinstance(value, tuple):
            return exp.Tuple(
                expressions=[self._to_sql_literal(v) for v in value]
            )

        raise TypeError(
            f"Unsupported value for SQL literal: {value!r} ({type(value)})"
        )

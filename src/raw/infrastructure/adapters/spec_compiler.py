from typing import Any
from datetime import datetime, date
from enum import Enum

from sqlglot import exp

from ...domain import FieldSpec, And, Or, Not, Spec


def eq(c: exp.Column, v: exp.Expression):
    if isinstance(v, exp.Null):
        return exp.Is(
            this=c,
            expression=exp.Null()
        )
    return exp.EQ(
        this=c,
        expression=v # value is already parsed to literal, no need to do it here
    )


OPERATOR_MAP = {
    "eq": lambda c, v: eq(c, v),
    "ne": lambda c, v: c.neq(v),
    "gt": lambda c, v: c > v,
    "gte": lambda c, v: c >= v,
    "lt": lambda c, v: c < v,
    "lte": lambda c, v: c <= v,
    "like": lambda c, v: c.like(v),
    "in": lambda c, v: c.isin(v),
}


class SpecCompilerSQL:
    def compile(self, spec: Spec):
        match spec:
            case FieldSpec(field=field, operator=op, value=value):
                return self._compile_field(field, op.value, value)

            case And(left=left, right=right):
                return exp.and_(self.compile(spec.left), self.compile(spec.right))

            case Or(left=left, right=right):
                return exp.or_(self.compile(spec.left), self.compile(spec.right))

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
            return exp.Literal.string(value.isoformat(sep=""))

        if isinstance(value, Enum):
            return exp.Literal.string(value.value)

        if isinstance(value, tuple):
            return exp.Tuple(
                expressions=[self._to_sql_literal(v) for v in value]
            )

        raise TypeError(
            f"Unsupported value for SQL literal: {value!r} ({type(value)})"
        )

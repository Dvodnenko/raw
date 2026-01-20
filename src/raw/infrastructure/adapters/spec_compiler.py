from typing import Any

from sqlglot import exp

from ...domain import FieldSpec, And, Or, Not, Spec


OPERATOR_MAP = {
    "eq": lambda f, v: f.eq(v),
    "ne": lambda f, v: f.neq(v),
    "gt": lambda f, v: f.gt(v),
    "gte": lambda f, v: f.gte(v),
    "lt": lambda f, v: f.lt(v),
    "lte": lambda f, v: f.lte(v),
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

    def _compile_field(field: str, operator: str, value: Any) -> exp.Expression:
        if operator not in OPERATOR_MAP:
            raise ValueError(f"Unsupported operator: {operator}")

        column = exp.column(field)

        if operator == "in":
            if not isinstance(value, (list, tuple, set)):
                raise TypeError("IN operator expects iterable value")

            literals = [exp.Literal(this=v) for v in value]
            return column.isin(exp.Tuple(expressions=literals))

        literal = exp.Literal(this=value)
        return OPERATOR_MAP[operator](column, literal)


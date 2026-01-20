from sqlalchemy import and_, or_, Table

from ...domain import FieldSpec, And, Or, Not, Spec


class SpecCompilerSA:
    def compile(self, spec: Spec, table: Table):
        if isinstance(spec, FieldSpec):
            return self._compile_field(spec, table)
        if isinstance(spec, And):
            return and_(self.compile(spec, table) for spec in spec.items)
        if isinstance(spec, Or):
            return or_(self.compile(spec, table) for spec in spec.items)
        if isinstance(spec, Not):
            return ~self.compile(spec.spec)
        raise TypeError(spec)

    def _compile_field(self, spec: FieldSpec, table: Table):
        try:
            column = getattr(table.c, spec.field)
        except AttributeError:
            raise ValueError(f"Field not found: {spec.field}") from None
        match spec.operator:
            case "==":
                return column == spec.value
            case "!=":
                return column != spec.value
            case ">":
                return column > spec.value
            case ">=":
                return column >= spec.value
            case "<":
                return column < spec.value
            case "<=":
                return column <= spec.value
            case "like":
                return column.like(spec.value)
            case "notlike":
                return column.notilike(spec.value)
            case "in":
                return column.in_(spec.value)
            case "notin":
                return column.notin_(spec.value)

        raise ValueError(spec.operator)

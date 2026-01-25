import re
import sqlite3
from dataclasses import dataclass
from enum import Enum


class ConstraintKind(Enum):
    UNIQUE = "unique"
    NOT_NULL = "not_null"
    FOREIGN_KEY = "foreign_key"
    CHECK = "check"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class IntegrityViolation:
    kind: ConstraintKind
    table: str | None
    column: str | None
    raw: str


_UNIQUE_RE = re.compile(r"UNIQUE constraint failed: (\w+)\.(\w+)")
_NOT_NULL_RE = re.compile(r"NOT NULL constraint failed: (\w+)\.(\w+)")
_CHECK_RE = re.compile(r"CHECK constraint failed: (\w+)")


def resolve_integrity_error(err: sqlite3.IntegrityError) -> IntegrityViolation:
    message = err.args[0]

    if m := _UNIQUE_RE.search(message):
        table, column = m.groups()
        return IntegrityViolation(
            kind=ConstraintKind.UNIQUE,
            table=table,
            column=column,
            raw=message,
        )

    if m := _NOT_NULL_RE.search(message):
        table, column = m.groups()
        return IntegrityViolation(
            kind=ConstraintKind.NOT_NULL,
            table=table,
            column=column,
            raw=message,
        )

    if "FOREIGN KEY constraint failed" in message:
        return IntegrityViolation(
            kind=ConstraintKind.FOREIGN_KEY,
            table=None,
            column=None,
            raw=message,
        )

    if m := _CHECK_RE.search(message):
        constraint = m.group(1)
        return IntegrityViolation(
            kind=ConstraintKind.CHECK,
            table=None,
            column=constraint,
            raw=message,
        )

    return IntegrityViolation(
        kind=ConstraintKind.UNKNOWN,
        table=None,
        column=None,
        raw=message,
    )

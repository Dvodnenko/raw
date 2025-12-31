from sqlalchemy.exc import IntegrityError, NoResultFound

from ..domain import UniquenessError, EntryNotFoundError


def unique_violation_column(exc: IntegrityError) -> str | None:
    msg = str(exc.orig)

    if "UNIQUE constraint failed:" not in msg:
        return None

    return msg.split(": ", 1)[1]


def handle_database_exceptions(func):

    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as exc:
            if col := unique_violation_column(exc):
                raise UniquenessError(col) from None
        except NoResultFound:
            raise EntryNotFoundError() from None

    return wrap

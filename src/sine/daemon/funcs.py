import traceback

import dateparser
from datetime import datetime


def asexc(e: Exception):
    """
    Prints an exception in a pretty way
    """
    
    return " ".join(p for p in traceback.format_exception(e, chain=True))


def cast_datetime(value: str):
    return (dateparser.parse(value) or \
        datetime.now()).replace(microsecond=0)

def is_(type_: type, other: type):
    return (type_ is other) or (issubclass(type_, other))

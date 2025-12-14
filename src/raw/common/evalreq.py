import hashlib
import datetime

from .config import config_
from .driller import drill
from .constants import DEFAULT_FSTRING_MARK


def rstr(length: int = 10):
    """
    Returns a random string
    """
    return hashlib.blake2b(
        bytes(datetime.datetime.now().isoformat(), encoding="utf-8"),
        digest_size=length//2,
    ).hexdigest()


FSTRING_MARK = drill(
    config_, ["general", "fstring_mark"], default=DEFAULT_FSTRING_MARK)

def evalreq_(argv: list[str]):
    for index, value in enumerate(argv):
        if not value.startswith(FSTRING_MARK):
            continue
        argv[index] = eval(f"f'{value[1:]}'", globals())
    return argv

import hashlib
import datetime


def rstr(length: int = 10):
    """
    Returns a random string
    """
    return hashlib.blake2b(
        bytes(datetime.datetime.now().isoformat(), encoding="utf-8"),
        digest_size=length//2,
    ).hexdigest()


def evalreq_(argv: list[str]):
    for index, value in enumerate(argv):
        if not ("{" in value and "}" in value):
            continue
        argv[index] = eval(f"f'{value}'", globals())
    return argv

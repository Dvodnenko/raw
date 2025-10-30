import sys

from .utils.parser import parse_cli_args
from .utils.resolve import resolve_callback
from .constants import SUPPORTED_SYSTEMS


def execute(callback, args, kwargs, flags):
    yield from callback(args, kwargs, flags)


@parse_cli_args
def raw(args, kwargs, flags):

    if not args:
        exit(0)

    if not sys.platform.lower() in SUPPORTED_SYSTEMS:
        print(f"Unsupported operating system: {sys.platform}")
        exit(1)

    callback = resolve_callback(args)

    error_ocurred: int = 0

    for response in execute(callback, args, kwargs, flags):
        print(response[0])
        if response[1] != 0: error_ocurred = 1

    exit(error_ocurred)

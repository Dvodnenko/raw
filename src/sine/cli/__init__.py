import sys

import halo

from .utils.resolve import resolve_callback
from ..common.constants import SUPPORTED_SYSTEMS
from ..common import generate_rspd, evalreq_


def execute(callback, rspd):

    spinner = halo.Halo(text="Loading...", spinner="dots", color="white", 
                        stream=sys.stderr)
    spinner.start()

    for i in callback(rspd):
        spinner.clear()
        yield i


def sin():

    argv = evalreq_(sys.argv[1:])
    rspd = generate_rspd(argv)

    try:
        if not argv:
            exit(0)

        if not sys.platform.lower() in SUPPORTED_SYSTEMS:
            print(f"Unsupported operating system: {sys.platform}")
            exit(1)

        callback = resolve_callback(rspd)

        error_ocurred: int = 0

        for response in execute(callback, rspd):
            print(response[0])
            if response[1] != 0: error_ocurred = 1

        exit(error_ocurred)
    except KeyboardInterrupt:
        print("Cancelled by user")
        exit(0)

from .icm import INTERNAL_CMD_MAP, drill
from .connection import request


def resolve_callback(args):
    """
    Find and return the callback that actually 
    runs the logic user is asking for

    If the callback is internal - return the 
    callback object itself; if its external - 
    prepare everything for request
    """

    callback = None

    if args[0] in INTERNAL_CMD_MAP.keys(): # user calls internal service
        callback = drill(INTERNAL_CMD_MAP, args)
    else: # need to make daemon request
        callback = request
    
    return callback

import argparse

from ...shared import MISSING
from ..constants import EDITOR_SENTINEL
from ..handlers.gas import handle_gas_cmd


def register_gas_cmd(sub: argparse._SubParsersAction):
    """
    "gas" means "get active sessions"
    """
    parser = sub.add_parser("gas",
        description="get active sessions",
        help="get active sessions")
    
    parser.add_argument("--orderby",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<field>",
        help="change output order"
    )
    parser.add_argument("-r",
        action="store_true",
        help="reverse output"
    )

    parser.set_defaults(handler=handle_gas_cmd)

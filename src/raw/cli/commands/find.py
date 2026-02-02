import argparse

from ...shared import MISSING
from ..constants import EDITOR_SENTINEL
from ..handlers.find import handle_find_cmd


def register_find_cmd(sub: argparse._SubParsersAction):
    parser = sub.add_parser("find",
        aliases=["print"],
        description="find entities by provided specification",
        help="find entities by provided specification")
    
    parser.add_argument("type")
    
    parser.add_argument("--where",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<specification>",
    )
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

    parser.set_defaults(handler=handle_find_cmd)

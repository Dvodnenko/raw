import argparse

from ...shared import MISSING
from ..constants import EDITOR_SENTINEL
from ..handlers.stop import handle_stop_cmd


def register_stop_cmd(sub: argparse._SubParsersAction):
    parser = sub.add_parser("stop",
        aliases=["end"],
        description="stop a work session",
        help="stop a work session")
    
    parser.add_argument(
        "identifier",
        help="id or title"
    )

    ## General Options, for All Entity Types
    common_options = parser.add_argument_group(
        "common options",
    )
    common_options.add_argument("--title",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<title>"
    )
    common_options.add_argument("--description",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<desc>"
    )
    common_options.add_argument("--icon",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<icon>"
    )

    ## Session Options
    session_options = parser.add_argument_group(
        "session options",
    )
    session_options.add_argument("--message",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<message>"
    )
    session_options.add_argument("--summary",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<summary>"
    )
    session_options.add_argument("--started_at",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<start time>"
    )
    session_options.add_argument("--ended_at",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<end time>"
    )

    parser.set_defaults(handler=handle_stop_cmd)

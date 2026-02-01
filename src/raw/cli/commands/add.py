import argparse

from ...shared import MISSING
from ..constants import EDITOR_SENTINEL
from ..handlers.add import handle_add_cmd


def register_add_cmd(sub: argparse._SubParsersAction):
    """
    Registers "add" CLI command and its options in provided subparser

    Handles creation of all types of entities
    """

    parser = sub.add_parser("add",
        description="create a new entity",
        help="create a new entity")
    
    parser.add_argument("type")

    ## General Options, for All Entity Types
    parser.add_argument("--title",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<title>"
    )
    parser.add_argument("--description",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<desc>"
    )
    parser.add_argument("--icon",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<icon>"
    )

    ## Task Options
    parser.add_argument("--status",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<status>"
    )
    parser.add_argument("--deadline",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<deadline>"
    )

    ## Note Options
    parser.add_argument("--content",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<content>"
    )

    parser.set_defaults(handler=handle_add_cmd)

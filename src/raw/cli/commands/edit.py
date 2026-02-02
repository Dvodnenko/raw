import argparse

from ...shared import MISSING
from ..constants import EDITOR_SENTINEL
from ..handlers.edit import handle_edit_cmd


def register_edit_cmd(sub: argparse._SubParsersAction):
    """
    Registers "edit" CLI command and its options in provided subparser
    """

    parser = sub.add_parser("edit",
        description="edit an entity",
        help="edit an entity")
    
    parser.add_argument("identifier")

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

    ## Session Options
    parser.add_argument("--message",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<message>"
    )
    parser.add_argument("--summary",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<summary>"
    )
    parser.add_argument("--started_at",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<start time>"
    )
    parser.add_argument("--ended_at",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<end time>"
    )

    parser.set_defaults(handler=handle_edit_cmd)

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
        aliases=["create"],
        description="create a new entity",
        help="create a new entity")
    
    parser.add_argument("type", choices=("task", "note", "session", "folder"))

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

    ## Task Options
    task_options = parser.add_argument_group(
        "task options",
    )
    task_options.add_argument("--status",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<status>"
    )
    task_options.add_argument("--deadline",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<deadline>"
    )

    ## Note Options
    note_options = parser.add_argument_group(
        "note options",
    )
    note_options.add_argument("--content",
        nargs="?",
        const=EDITOR_SENTINEL,
        default=MISSING,
        metavar="<content>"
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

    parser.set_defaults(handler=handle_add_cmd)

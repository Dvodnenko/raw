import argparse

from .commands.init import register_init_cmd
from .commands.add import register_add_cmd
from .commands.edit import register_edit_cmd


def build_parser():
    parser = argparse.ArgumentParser(
        prog="raw",
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True
    )

    parser.add_argument("-D", action="store_true", help="run script in debug mode")
    register_init_cmd(sub)
    register_add_cmd(sub)
    register_edit_cmd(sub)

    return parser

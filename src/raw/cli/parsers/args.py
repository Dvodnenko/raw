import argparse

from ..commands.init import register_init_cmd
from ..commands.add import register_add_cmd
from ..commands.find import register_find_cmd
from ..commands.edit import register_edit_cmd
from ..commands.remove import register_remove_cmd


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
    register_find_cmd(sub)
    register_edit_cmd(sub)
    register_remove_cmd(sub)

    return parser

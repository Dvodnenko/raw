import argparse

from ..commands.init import register_init_cmd
from ..commands.sql import register_sql_cmd
from ..commands.add import register_add_cmd
from ..commands.find import register_find_cmd
from ..commands.gas import register_gas_cmd
from ..commands.edit import register_edit_cmd
from ..commands.remove import register_remove_cmd
from ..commands.start import register_start_cmd
from ..commands.stop import register_stop_cmd


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(message)
        exit(1)


def build_parser():
    parser = ArgumentParser(
        prog="raw",
        description="unstable lifeos",
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
    register_sql_cmd(sub)
    register_add_cmd(sub)
    register_find_cmd(sub)
    register_gas_cmd(sub)
    register_edit_cmd(sub)
    register_remove_cmd(sub)
    register_start_cmd(sub)
    register_stop_cmd(sub)

    return parser

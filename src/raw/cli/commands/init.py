import argparse

from ..handlers.init import handle_init_cmd


def register_init_cmd(sub: argparse._SubParsersAction):
    parser = sub.add_parser("init", help="initialize database")

    parser.set_defaults(handler=handle_init_cmd)

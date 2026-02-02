import argparse

from ..handlers.sql import handle_sql_cmd


def register_sql_cmd(sub: argparse._SubParsersAction):
    parser = sub.add_parser("sql", help="execute raw sql queries")

    parser.set_defaults(handler=handle_sql_cmd)

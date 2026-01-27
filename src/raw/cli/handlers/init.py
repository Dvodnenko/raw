import argparse
import sqlite3

from ...config import DB_PATH


def handle_init_cmd(args: argparse.Namespace):
    from ...infrastructure import create_tables

    with sqlite3.connect(DB_PATH) as conn:
        create_tables(conn)

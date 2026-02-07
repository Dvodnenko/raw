import argparse
import sqlite3

from ...config import DB_PATH


def handle_init_cmd(args: argparse.Namespace):
    from ...infrastructure import create_tables, create_db_file

    with sqlite3.connect(DB_PATH) as conn:
        create_db_file(DB_PATH)
        create_tables(conn)

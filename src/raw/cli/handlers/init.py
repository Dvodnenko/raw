import argparse
import sqlite3
from pathlib import Path

from ...config import config


def handle_init_cmd(args: argparse.Namespace):
    from ...infrastructure import create_tables, create_db_file

    create_db_file(Path(config["core"]["database"]))
    with sqlite3.connect(config["core"]["database"]) as conn:
        create_tables(conn)

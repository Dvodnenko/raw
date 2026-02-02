import argparse
import sys
import subprocess

from ...config import DB_PATH


def handle_sql_cmd(args: argparse.Namespace):
    subprocess.run(
        ["sqlite3", DB_PATH],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

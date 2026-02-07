import argparse
import sys
import subprocess

from ...config import config


def handle_sql_cmd(args: argparse.Namespace):
    subprocess.run(
        ["sqlite3", config["core"]["database"]],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

import argparse


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

    return parser

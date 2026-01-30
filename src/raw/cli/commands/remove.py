import argparse

from ..handlers.remove import handle_remove_cmd


def register_remove_cmd(sub: argparse._SubParsersAction):
    parser = sub.add_parser("remove",
        description="remove an entity",
        help="remove an entity")
    
    parser.add_argument("id", type=int)

    parser.set_defaults(handler=handle_remove_cmd)

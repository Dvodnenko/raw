import argparse

from ...application import Remove, RemoveCmd, Identifier
from ...infrastructure import UnitOfWorkSQL
from ...config import config


def handle_remove_cmd(args: argparse.Namespace):

    identifier: int = args.identifier

    cmd = RemoveCmd(Identifier(identifier))
    interactor = Remove(UnitOfWorkSQL(config["core"]["database"]))

    interactor.remove(cmd)

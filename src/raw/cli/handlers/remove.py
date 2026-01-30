import argparse

from ...application import RemoveEntity, RemoveEntityCmd
from ...infrastructure import UnitOfWorkSQL
from ...config import DB_PATH


def handle_remove_cmd(args: argparse.Namespace):

    id: int = args.id

    cmd = RemoveEntityCmd(id=id)
    interactor = RemoveEntity(UnitOfWorkSQL(DB_PATH))

    interactor.remove(cmd)

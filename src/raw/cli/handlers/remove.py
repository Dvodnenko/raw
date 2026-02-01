import argparse

from ...application import Remove, RemoveCmd
from ...infrastructure import UnitOfWorkSQL
from ...config import DB_PATH


def handle_remove_cmd(args: argparse.Namespace):

    id: int = args.id

    cmd = RemoveCmd(id=id)
    interactor = Remove(UnitOfWorkSQL(DB_PATH))

    interactor.remove(cmd)

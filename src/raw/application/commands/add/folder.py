from dataclasses import dataclass
from typing import Optional

from ....domain import (
    Folder, UnitOfWork,
    NotFound, AlreadyExists, EntityRef
)
from ...common import _extract_parent_title


@dataclass(frozen=True)
class AddFolderCmd:
    title: Optional[str] = ""
    description: Optional[str] = ""
    icon: Optional[str] = ""

class AddFolder:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add(self, cmd: AddFolderCmd):
        obj = Folder(
            # repository will generate the id by itself 
            # and we don't really need it here
            id=None,
            title=cmd.title,
            description=cmd.description,
            icon=cmd.icon,
        )

        parent_path: Optional[str] = _extract_parent_title(cmd.title)

        with self.uow:
            already_exists = self.uow.intertype.resolve_type_by_title(obj.title) is not None
            if already_exists:
                raise AlreadyExists(EntityRef(obj.title))

            if parent_path:
                parent_id = self.uow.intertype.resolve_id_by_title(parent_path)
                if not parent_id:
                    raise NotFound(EntityRef(parent_path))
                obj.parent_id = parent_id

            self.uow.folders.add(obj)

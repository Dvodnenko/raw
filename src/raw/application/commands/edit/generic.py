from dataclasses import dataclass
from typing import Any

from ....domain import (
    UnitOfWork, TaskEditor, NoteEditor, NotFound,
    EntityRef, EntityType, SessionEditor, FolderEditor)
from ...identifier import Identifier
from .task import EditTask, EditTaskCmd
from .note import EditNote, EditNoteCmd
from .session import EditSession, EditSessionCmd
from .folder import EditFolder, EditFolderCmd


@dataclass(frozen=True)
class EditEntityCmd:
    identifier: Identifier
    fields: dict[str, Any]

class EditEntity:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def edit(self, cmd: EditEntityCmd):
        with self.uow:
            if cmd.identifier.is_id:
                type = self.uow.intertype.resolve_type(int(cmd.identifier.value))
            else:
                type = self.uow.intertype.resolve_type_by_title(cmd.identifier.value)

        if not type:
            raise NotFound(EntityRef(cmd.identifier.value))
        
        match type:
            case EntityType.TASK:
                cmd = EditTaskCmd(
                    cmd.identifier,
                    TaskEditor(**cmd.fields)
                )
                EditTask(self.uow).edit(cmd)
            case EntityType.NOTE:
                cmd = EditNoteCmd(
                    cmd.identifier,
                    NoteEditor(**cmd.fields)
                )
                EditNote(self.uow).edit(cmd)
            case EntityType.SESSION:
                cmd = EditSessionCmd(
                    cmd.identifier,
                    SessionEditor(**cmd.fields)
                )
                EditSession(self.uow).edit(cmd)
            case EntityType.FOLDER:
                cmd = EditFolderCmd(
                    cmd.identifier,
                    FolderEditor(**cmd.fields)
                )
                EditFolder(self.uow).edit(cmd)

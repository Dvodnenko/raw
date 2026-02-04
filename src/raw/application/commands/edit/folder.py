from dataclasses import dataclass
from typing import Optional

from ....domain import (
    Folder, UnitOfWork, FolderEditor, NotFound,
    InvalidState, EntityRef, AlreadyExists
)
from ...common import _extract_parent_title
from ....shared import MISSING
from ...identifier import Identifier


@dataclass(frozen=True)
class EditFolderCmd:
    identifier: Identifier
    editor: FolderEditor

class EditFolder:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def edit(self, cmd: EditFolderCmd):
        with self.uow:
            # 1. check if the folder even exists
            folder: Optional[Folder] = None
            if cmd.identifier.is_title:
                folder = self.uow.folders.get_by_title(cmd.identifier.value)
            else:
                folder = self.uow.folders.get_by_id(int(cmd.identifier.value))
            if not folder:
                raise NotFound(EntityRef(cmd.identifier.value))
            
            # 2. remember its old title and parent's old title, in case user edits it
            old_title = folder.title
            old_parent_path: Optional[str] = _extract_parent_title(old_title)

            # 3. register optional value of new parent, if it is edited also
            new_parent_path: Optional[str] = None

            if cmd.editor.title is not MISSING: # user tries to edit the title
                if cmd.editor.title.startswith(folder.title+"/"): # ! user tries to move folder into itself
                    raise InvalidState("cannot move folder into itself")
                already_exists = (
                    self.uow.intertype
                    .resolve_type_by_title(cmd.editor.title)
                ) is not None
                if already_exists:
                    raise AlreadyExists(EntityRef(cmd.editor.title))
            edited = cmd.editor.apply(folder)
            # check if user changed parent
            # or only title of folder itself (only title = last title segment,
            # in "/a/b/c" it's "c")
            new_parent_path = _extract_parent_title(edited.title)
            if new_parent_path != old_parent_path: # parent changed
                # checking if the new parent exists
                new_parent_id = self.uow.intertype.resolve_id_by_title(new_parent_path)
                if not new_parent_id:
                    raise NotFound(EntityRef(new_parent_path))
                # parent id changes ONLY if:
                # 1. parent title was changed
                # 2. new parent exists
                edited.parent_id = new_parent_id

            self.uow.folders.save(edited)

            if old_title != edited.title:
                self.uow.intertype.rewrite_subtree_titles(
                    old_prefix=old_title,
                    new_prefix=edited.title,
                )

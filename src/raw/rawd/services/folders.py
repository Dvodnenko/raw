from ..entities import Response
from ..repositories.folder import saFolderRepository
from ..database.mappings.folder import Folder
from ..database.session import Session


class FolderService:
    def __init__(self):
        self.repository = saFolderRepository(Session())

    def create(self, args: list, flags: list, **kwargs) -> Response:
        folder = Folder(**kwargs)
        if self.repository.get(folder.title):
            return Response(f"Folder already exists: {folder.title}")
        if folder.parentstr != "":
            if not self.repository.get(folder.parentstr):
                return Response(f"Folder not found: {folder.parentstr}")
        self.repository.create(folder)
        return Response(f"Folder created: {folder.title}")
    
    def get(self, args: list, flags: list, **kwargs) -> Folder | None:
        return self.repository.get(args[0])
        
    def update(self, args: list, flags: list, **kwargs):
        current = self.repository.get(args[0])
        if not current:
            return Response(f"Folder not found: {args[0]}")
        self.repository.update(args[0], **kwargs)
        return Response(f"Folder updated: {args[0]}")

    def delete(self, args: list, flags: list, **kwargs):
        folder = self.repository.get(args[0])
        delete = False
        if not folder:
            return Response(f"Folder not found: {args[0]}")
        if folder.children:
            if "F" in flags:
                delete = True
        else: delete = True
        if delete:
            self.repository.delete(folder)
            return Response(f"Folder deleted: {args[0]}")
        else:
            return Response(f"Cannot delete Folder '{args[0]}' because it is not empty")

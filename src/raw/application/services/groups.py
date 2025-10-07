from pathlib import Path

from ...domain import (
    Group, EntityRepository, Config, UseCaseResponse
)

class GroupService:
    def __init__(
            self, 
            repository: EntityRepository, 
            config: Config
    ):
        self.repository = repository
        self.config = config

    def create(self, group: Group) -> UseCaseResponse:
        if self.repository.get(group.title):
            return UseCaseResponse(f"Group already exists: {group.title}", status_code=5)
        if not group.parentstr == "":
            if not self.repository.get(group.parent):
                return UseCaseResponse(f"Group not found: {group.parent}", status_code=4)
        self.repository.create(group)
        return UseCaseResponse(f"Group created: {group.title}")
    
    def get(self, title: str) -> Group | None:
        return self.repository.get(title)
        
    def update(self, title: Path, new: Group):
        if not self.repository.get(title):
            return UseCaseResponse(f"Group not found: {title}", status_code=4)
        if self.repository.get(new.title):
            return UseCaseResponse(f"Group already exists: {new.title}", status_code=5)
        self.repository.update(title, new)
        return UseCaseResponse(f"Group updated: {title}")

    def delete(self, title: Path, force: bool = False):
        group = self.repository.get(title)
        if not group:
            return UseCaseResponse(f"Group not found: {title}", status_code=4)
        if group.children:
            if force:
                self.repository.delete(group)
            else:
                return UseCaseResponse(f"Cannot delete Group '{title}' because it is not empty")
        return UseCaseResponse(f"Group deleted: {title}")

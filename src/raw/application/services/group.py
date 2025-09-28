import shutil

from ...domain import Group, EntityRepository, Config, UseCaseResponse


class GroupService:
    def __init__(self, repo: EntityRepository, config: Config):
        self.repo = repo
        self.config = config

    def create(self, group: Group) -> UseCaseResponse[Group]:
        _path = self.config.core.rootgroup / group.subpath
        if _path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Group already exists: {group.subpath}", 
            )
        _path.mkdir(parents=True)
        (_path / f"self.{self.repo.ext}").touch()
        self.repo.dump(self.config.core.rootgroup, group)
        return UseCaseResponse(
            message=f"Group created: {group.subpath}"
        )
    
    def update(self, subpath: str, new: Group) -> UseCaseResponse[Group]:
        current_path = self.config.core.rootgroup / subpath
        if not current_path.exists() or not current_path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {subpath}", status_code=4
            )
        destination = self.config.core.rootgroup / new.subpath
        destination_self = (destination / f"self.{self.repo.ext}")
        if current_path != destination:
            self.repo.mv(current_path, destination)
            destination_self.parent.mkdir()
            destination_self.touch()
        self.repo.dump(self.config.core.rootgroup, new)
        return UseCaseResponse(
            message=f"Group updated: {subpath}"
        )
    
    def delete(self, subpath: str) -> UseCaseResponse[Group]:
        _path = self.config.core.rootgroup / subpath
        if not _path.exists() or not _path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {subpath}", status_code=4
            )
        shutil.rmtree(_path)
        return UseCaseResponse(
            message=f"Group deleted: {subpath}"
        )

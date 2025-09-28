from ...domain import Tag, EntityRepository, Config, UseCaseResponse


class TagService:
    def __init__(self, repo: EntityRepository, config: Config):
        self.repo = repo
        self.config = config
        self.prefix = "TAG-"
    
    def create(self, tag: Tag) -> UseCaseResponse[Tag]:
        _path = self.config.core.raw_path / tag.subpath / f"{self.prefix}{tag.title}.{self.repo.ext}"
        if _path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Tag already exists: {tag.subpath}/{tag.title}", 
            )
        _path.touch()
        self.repo.dump(tag)
        return UseCaseResponse(
            message=f"Tag created: {tag.subpath}/{tag.title}"
        )
    
    def update(self, subpath: str, new: Tag) -> UseCaseResponse[Tag]:
        current_path = self.config.core.raw_path / subpath / f"{self.prefix}{new.title}.{self.repo.ext}"
        if not current_path.exists() or not current_path.is_file():
            return UseCaseResponse(
                message=f"Tag not found: {subpath}", status_code=4
            )
        new_path = self.config.core.raw_path / new.subpath / f"{self.prefix}{new.title}.{self.repo.ext}"
        if new_path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Tag already exists: {new.subpath}/{new.title}", 
            )
        self.repo.mv(current_path, new_path)
        self.repo.dump(new)
        return UseCaseResponse(
            message=f"Tag updated: {subpath}"
        )
    
    def delete(self, subpath: str) -> UseCaseResponse[Tag]:
        _path = self.config.core.raw_path / f"{self.prefix}{subpath}.{self.repo.ext}"
        if not _path.exists() or not _path.is_file():
            return UseCaseResponse(
                message=f"Tag not found: {subpath}", status_code=4
            )
        _path.unlink()
        return UseCaseResponse(
            message=f"Tag deleted: {subpath}"
        )

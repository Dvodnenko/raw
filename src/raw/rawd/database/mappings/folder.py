from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..orm_registry import mapping_registry


@mapping_registry.mapped_as_dataclass
class Folder:
    __tablename__ = "folders"

    id: Mapped[int] = mapped_column(
        ForeignKey("entities.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "folder",
    }

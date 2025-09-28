from abc import ABC, abstractmethod
from pathlib import Path

from ..base.entity import Entity


class EntityRepository(ABC):

    ext: str = None
    
    @abstractmethod
    def dump(self, rootgroup: Path, entity: Entity) -> None: ...

    @abstractmethod
    def load(self, path: Path) -> Entity: ...

    @abstractmethod
    def mv(self, current: Path, new: Path) -> None: ...

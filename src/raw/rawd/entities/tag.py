from dataclasses import dataclass

from .entity import Entity


@dataclass(kw_only=True, eq=False)
class Tag(Entity):

    def to_dict(self):
        return {
            ## From Entity
            **super().to_dict(),
        }

from dataclasses import dataclass, field

from .entity import Entity


@dataclass(kw_only=True, eq=False)
class Folder(Entity):
    children: list["Entity"] = field(
        default_factory=lambda: [])

    def to_dict(self):
        return {
            ## From Entity
            "title": self.title,
            "color": self.color,
            "icon": self.icon,
            "description": self.description,
            "links": self.links,
            "parent": self.parent,
            "parent_id": self.parent_id,

            # Folder's itself
            "children": self.children
        }

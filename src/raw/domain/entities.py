from dataclasses import dataclass, field
from datetime import datetime

from .value_objects import Styles
from .enums import TaskStatus


def now() -> datetime:
    return datetime.now().replace(microsecond=0)


@dataclass(kw_only=True)
class Entity:
    id: int
    title: str
    description: str = ""
    styles: Styles = Styles()
    icon: str = ""
    links: set[int] = field(default_factory=set)

    def __post_init__(self):
        if self.title == "" or self.title.strip() == "":
            raise ValueError("Title cannot be empty")
        
    def link(self, links: set[int]):
        self.links = links

    def add_links(self, links: set[int]):
        self.links.update(links)
    
    def remove_links(self, links: set[int]):
        self.links.difference_update(links)


@dataclass(kw_only=True)
class Task(Entity):
    
    status: TaskStatus = TaskStatus.ACTIVE
    deadline: datetime = None

    def mark(self, value: str):
        try:
            self.status = TaskStatus(value)
        except ValueError:
            raise ValueError(f"No such status: {value}") from None

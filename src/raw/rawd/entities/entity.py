from dataclasses import dataclass, field
from hashlib import blake2b
from datetime import datetime

from .enums import Color


def generate_title():
    return blake2b(
        digest_size=20,
        data=bytes(datetime.now().isoformat(), encoding="utf-8")
    ).hexdigest()


@dataclass(eq=False)
class Entity:

    title: str = field(default_factory=generate_title) # /a/b/c, not just c
    color: Color = Color.WHITE
    icon: str = ""
    description: str = ""

    links: list["Entity"] = field(
        default_factory=lambda: [])
    parent_id: int = None
    parent: "Folder" = None

    def __post_init__(self):
        if not self.title.startswith("/"):
            self.title = f"/{self.title}"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        self.__post_init__()
        return self

    @property
    def parentstr(self) -> str:
        return self.title[0:self.title.rfind("/")]

    @property
    def name(self) -> str:
        return self.title[self.title.rfind("/")+1 :]

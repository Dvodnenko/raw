from dataclasses import dataclass, field


@dataclass(eq=False)
class Entity:

    title: str # /a/b/c, not just c
    styles: str = ""
    icon: str = ""
    description: str = ""

    id: int = None
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

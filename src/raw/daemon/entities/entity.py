from dataclasses import dataclass


@dataclass(eq=False)
class Entity:

    title: str # /a/b/c, not just c
    styles: str = ""
    icon: str = ""
    description: str = ""

    id: int = None
    parent_id: int = None
    type: str = None
    links: list["Entity"] = None

    def __post_init__(self):
        if not self.title.startswith("/"):
            self.title = f"/{self.title}"

    @property
    def desc(self):
        return self.description
    
    @desc.setter
    def desc(self, value):
        self.description = value

    @property
    def parentstr(self) -> str:
        return self.title[0:self.title.rfind("/")]

    @property
    def name(self) -> str:
        return self.title[self.title.rfind("/")+1 :]

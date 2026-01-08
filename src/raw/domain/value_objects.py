from dataclasses import dataclass


@dataclass(frozen=True)
class Styles:
    
    r: int = 255
    g: int = 255
    b: int = 255

    bold: bool = False
    cursive: bool = False
    underlined: bool = False

    def __post_init__(self):
        if not (
            0 <= self.r <= 255 and
            0 <= self.g <= 255 and
            0 <= self.b <= 255
        ):
            raise ValueError("RGB values must be in range [0;255]")

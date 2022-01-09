from os.path import join
from PIL.ImageFont import truetype, FreeTypeFont
from os import getcwd
print(getcwd())
print(__file__)


class Font:
    def __init__(self, file: str) -> None:
        self.file = file

    def pil(self, fontsize: float) -> FreeTypeFont:
        return truetype(self.file, int(fontsize))


class Fonts:
    CascadiaCode: Font = Font(join("Fonts", "Cascadia", "CascadiaCode.ttf"))

from os.path import join, dirname
from PIL.ImageFont import truetype, FreeTypeFont


print(__file__)
print(dirname(__file__))


class Font:
    def __init__(self, file: str) -> None:
        self.file = file
        print(self.file)

    def pil(self, fontsize: float) -> FreeTypeFont:
        return truetype(self.file, int(fontsize))


class Fonts:
    CascadiaCode: Font = Font(join("..", "Fonts", "Cascadia", "CascadiaCode.ttf"))

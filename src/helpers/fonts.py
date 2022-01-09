from os.path import join, curdir
from PIL.ImageFont import truetype, FreeTypeFont

print(curdir)


class Font:
    def __init__(self, file: str) -> None:
        self.file = file

    def pil(self, fontsize: float) -> FreeTypeFont:
        return truetype(self.file, int(fontsize))


class Fonts:
    CascadiaCode: Font = Font(join(curdir, "Fonts", "Cascadia", "CascadiaCode.ttf"))

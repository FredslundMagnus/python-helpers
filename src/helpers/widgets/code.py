from __future__ import annotations
from helpers.colors import Colors, Color
from helpers.fonts import Font, Fonts
from helpers.widgets.languages import Language, Languages
from helpers.widgets.widget import *


class Code(Widget):
    def __init__(self, code: str, language: Language = Languages.python, fontSize: float = 16.0) -> None:
        self.code = code
        self.fontSize = fontSize
        self.font: Font = Fonts.CascadiaCode
        self.language = language
        self.size = Size(*self.font.pil(self.fontSize).getsize(self.code))
        print(self.size)
        super().__init__()

    @staticmethod
    def fromFile(filename: str, fontSize: float = 16.0) -> Code:
        with open(filename) as f:
            code = f.read()
        return Code(code, language=Languages.fromExtension(filename.split('.')[-1]), fontSize=fontSize)

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        canvas.text((offset.dx*ratio, offset.dy*ratio), self.text, self.color.color, self.font.pil(self.fontSize * ratio))


# class Text(Widget):
#     def __init__(self, text: str, fontSize: float = 16.0, color: Color = Colors.gray.c300, font: Font = Fonts.CascadiaCode) -> None:
#         self.text = text
#         self.fontSize = fontSize
#         self.color = color
#         self.font = font
#         self.size = Size(*self.font.pil(self.fontSize).getsize(self.text))
#         super().__init__()

#     def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
#         canvas.text((offset.dx*ratio, offset.dy*ratio), self.text, self.color.color, self.font.pil(self.fontSize * ratio))

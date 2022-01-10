from __future__ import annotations
from helpers.colors import Colors, Color
from helpers.fonts import Font, Fonts
from helpers.widgets.languages import Language, Languages
from helpers.widgets.widget import *


class Code(Widget):
    def __init__(self, code: str, language: Language = Languages.python, fontSize: float = 16.0, lineHeight: float = 1.5) -> None:
        self.code = code
        self.fontSize = fontSize
        self.font: Font = Fonts.CascadiaCode
        self.lineHeight = lineHeight
        self.language = language
        self.lines = self.code.splitlines()
        _size = self.font.pil(10000).getsize("m")
        self.charWidth = fontSize/_size[1]*_size[0]
        self.size = Size(self.charWidth*max(len(line) for line in self.lines), fontSize*(len(self.lines) + (len(self.lines)-1)*(self.lineHeight-1.0)))
        self.colors: list[list[Color]] = self.language.colorize(self.code)
        super().__init__()

    @staticmethod
    def fromFile(filename: str, fontSize: float = 16.0, lineHeight: float = 1.5) -> Code:
        with open(filename) as f:
            code = f.read()
        return Code(code, language=Languages.fromExtension(filename.split('.')[-1]), fontSize=fontSize, lineHeight=lineHeight)

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        for y, (line, colors) in enumerate(zip(self.lines, self.colors)):
            for x, (char, color) in enumerate(zip(line, colors)):
                canvas.text(((offset.dx + x*self.charWidth)*ratio, (offset.dy + y*self.fontSize*self.lineHeight)*ratio), char, color.color, self.font.pil(self.fontSize * ratio))


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

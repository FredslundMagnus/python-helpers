from __future__ import annotations
from helpers.colors import Colors, Color
from helpers.fonts import Font, Fonts
from helpers.widgets.languages import Language, Languages
from helpers.widgets.widget import *


class Code(Widget):
    def __init__(self, code: str, language: Language = Languages.python, fontSize: float = 16.0, lineHeight: float = 1.5, functions: set[str] = {}, classes: set[str] = {}) -> None:
        self.code = code
        self.fontSize = fontSize
        self.font: Font = Fonts.CascadiaCode
        self.lineHeight = lineHeight
        self.language = language
        self.lines = self.code.splitlines()
        _size = self.font.pil(10000).getsize("m")
        self.charWidth = fontSize/_size[1]*_size[0]
        self.size = None
        if self.fontSize != float("inf"):
            self.size = Size(self.charWidth*max(len(line) for line in self.lines), fontSize*(len(self.lines) + (len(self.lines)-1)*(self.lineHeight-1.0)))
        self.colors: list[list[Color]] = self.language.colorize(self.code, functions, classes)
        super().__init__()

    @staticmethod
    def fromFile(filename: str, fontSize: float = 16.0, lineHeight: float = 1.5, functions: set[str] = {}, classes: set[str] = {}) -> Code:
        with open(filename) as f:
            code = f.read()
        return Code(code, language=Languages.fromExtension(filename.split('.')[-1]), fontSize=fontSize, lineHeight=lineHeight, functions=functions, classes=classes)

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        for fontsize in range(1, 1000):
            print(self.charWidth*max(len(line) for line in self.lines))
            size = Size(self.charWidth*max(len(line) for line in self.lines), fontsize*(len(self.lines) + (len(self.lines)-1)*(self.lineHeight-1.0)))
            print(size, max_size)
            if size.width > max_size.width or size.height > max_size.height:
                break
        print(fontsize)
        fontsize -= 1
        print(fontsize)
        font = self.font.pil(fontsize * ratio)
        for y, (line, colors) in enumerate(zip(self.lines, self.colors)):
            for x, (char, color) in enumerate(zip(line, colors)):
                canvas.text(((offset.dx + x*self.charWidth)*ratio, (offset.dy + y*self.fontSize*self.lineHeight)*ratio), char, color.color, font)

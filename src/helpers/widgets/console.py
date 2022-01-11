from __future__ import annotations
from helpers.colors import Colors, Color
from helpers.fonts import Font, Fonts
from helpers.widgets.languages import Language, Languages
from helpers.widgets.widget import *


class Console(Widget):
    def __init__(self, code: str, fontSize: float = 16.0, lineHeight: float = 1.5, fitLines: int | None = None) -> None:
        self.code = code
        self.fontSize = fontSize
        self.font: Font = Fonts.CascadiaCode
        self.lineHeight = lineHeight
        self.lines = self.code.splitlines()
        if fitLines is not None:
            self.fontSize = float('inf')
            for _ in range(fitLines - len(self.lines)):
                self.lines.append("")
        _size = self.font.pil(10000).getsize("m")
        self.charWidth = None
        self.size = None
        if self.fontSize != float("inf"):
            self.charWidth = fontSize/_size[1]*_size[0]
            self.size = Size(self.charWidth*max(len(line) for line in self.lines), fontSize*(len(self.lines) + (len(self.lines)-1)*(self.lineHeight-1.0)))
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        if self.size is None:
            _size = self.font.pil(10000).getsize("m")
            for fontsize in range(1, 1000):
                _size = self.font.pil(10000).getsize("m")
                charWidth = fontsize/_size[1]*_size[0]
                size = Size(charWidth*max(len(line) for line in self.lines), fontsize*(len(self.lines) + (len(self.lines)-1)*(self.lineHeight-1.0)))
                if size.width > max_size.width or size.height > max_size.height:
                    break
            temp = fontsize - 1
            for adder in range(1002):
                fontsize = temp + adder/1000
                _size = self.font.pil(10000).getsize("m")
                charWidth = fontsize/_size[1]*_size[0]
                size = Size(charWidth*max(len(line) for line in self.lines), fontsize*(len(self.lines) + (len(self.lines)-1)*(self.lineHeight-1.0)))
                if size.width > max_size.width or size.height > max_size.height:
                    break
            self.fontSize = fontsize - 1/1000
            self.charWidth = self.fontSize/_size[1]*_size[0]
        font = self.font.pil(self.fontSize * ratio)
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                canvas.text(((offset.dx + x*self.charWidth)*ratio, (offset.dy + y*self.fontSize*self.lineHeight)*ratio), char, Colors.white.color, font)

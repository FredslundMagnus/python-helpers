from helpers.widgets.widget import *
from helpers.colors import Color, Colors
from helpers.fonts import Font, Fonts


class Text(Widget):
    def __init__(self, text: str, fontSize: float = 16.0, color: Color = Colors.gray.c300, font: Font = Fonts.CascadiaCode) -> None:
        self.text = text
        self.fontSize = fontSize
        self.color = color
        self.font = font
        self.lines = self.text.splitlines()
        _size = self.font.pil(10000).getsize("m")
        self.charWidth = fontSize/_size[1]*_size[0]
        self.size = Size(self.charWidth*max(len(line) for line in self.lines), fontSize*len(self.lines))
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                canvas.text(((offset.dx + x*self.charWidth)*ratio, (offset.dy + y*self.fontSize)*ratio), char, self.color.color, self.font.pil(self.fontSize * ratio))

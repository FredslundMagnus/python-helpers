from helpers.widgets.widget import *
from helpers.colors import Color, Colors
from helpers.fonts import Font, Fonts


class Text(Widget):
    def __init__(self, text: str, fontSize: float = 16.0, color: Color = Colors.gray.c300, font: Font = Fonts.CascadiaCode) -> None:
        self.text = text
        self.fontSize = fontSize
        self.color = color
        self.font = font
        self.size = Size(*self.font.pil(self.fontSize).getsize(self.text))
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        canvas.text((offset.dx*ratio, offset.dy*ratio), self.text, self.color.color, self.font.pil(self.fontSize * ratio))

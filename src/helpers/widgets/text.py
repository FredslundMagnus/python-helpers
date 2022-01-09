from helpers.widgets.widget import *
from helpers.colors import Color, Colors
from PIL.ImageFont import truetype as font


class Text(Widget):
    def __init__(self, text: str, fontSize: float = 16, color: Color = Colors.white, fontType: str = "arial.ttf") -> None:
        self.text = text
        self.fontSize = fontSize
        self.color = color
        self.fontType = fontType
        self.size = Size(*font(fontType, fontSize).getsize(text))
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        self.font = font(self.fontType, self.fontSize * ratio)
        canvas.text((offset.dx*ratio, offset.dy*ratio), self.text, self.color.color)

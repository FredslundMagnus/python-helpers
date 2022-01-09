from helpers.widgets.widget import *
from helpers.colors import Color, Colors
from PIL.ImageFont import truetype as font


class Text(Widget):
    def __init__(self, text: str, fontSize: float = 16, color: Color = Colors.white) -> None:
        self.text = text
        # self.fontSize = fontSize
        self.color = color
        self.font = font("arial.ttf", fontSize)
        print(self.font.getsize(text))
        self.size = Size(*self.font.getsize(text))
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        canvas.text((offset.dx*ratio, offset.dy*ratio), self.text, self.color.color)

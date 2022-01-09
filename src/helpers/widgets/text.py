from helpers.widgets.widget import *
from helpers.colors import Color, Colors
from PIL.ImageFont import truetype as create_font
from helpers.fonts import Font, Fonts


class Text(Widget):
    def __init__(self, text: str, fontSize: float = 16.0, color: Color = Colors.white, font: Font = Fonts.CascadiaCode) -> None:
        self.text = text
        self.fontSize = fontSize
        self.color = color
        self.fontType = font.file
        self.size = Size(*create_font(self.fontType, int(self.fontSize)).getsize(self.text))
        print(self.size)
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        self.font = create_font(self.fontType, int(self.fontSize * ratio))
        canvas.text((offset.dx*ratio, offset.dy*ratio), self.text, self.color.color, self.font)

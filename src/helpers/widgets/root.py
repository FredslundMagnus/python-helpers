from __future__ import annotations
from helpers.colors import Colors
from helpers.widgets.widget import Widget
from helpers.widgets.size import Size
from helpers.widgets.offset import Offset
from PIL import Image as IMG, ImageDraw
from PIL.Image import Image


class Root:
    def __init__(self, x_0: float, y_0: float, x_1: float, y_1: float, child: Widget) -> None:
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1
        self.size = Size((x_1-x_0) * 120, (y_1-y_0) * 120)  # Size((x_1-x_0) * 119.5, (y_1-y_0) * 119.9)
        self.offset = Offset(x_0 * 120, y_0 * 120)
        self.child = child
        super().__init__()

    def draw(self, size: tuple[int, int] = (1920, 1080), test: bool = False) -> Image:
        img = IMG.new('RGBA', size, (0, 0, 0, 0))
        canvas = ImageDraw.Draw(img)
        ratio = (size[1] / 1080)
        if test:
            canvas.rectangle((self.offset.dx*ratio, self.offset.dy*ratio, (self.offset.dx + self.size.width)*ratio, (self.offset.dy + self.size.height)*ratio), Colors.gray.c800.color)
        self.child.draw(canvas, self.offset, self.size, ratio)

        return img

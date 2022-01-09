from __future__ import annotations
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
        self.size = Size((x_1-x_0) * 119.5, (y_1-y_0) * 119.5)
        self.offset = Offset(x_0 * 120, y_0 * 120)
        self.child = child
        super().__init__()

    def draw(self, size: tuple[int, int] = (1920, 1080)) -> Image:
        img = IMG.new('RGBA', size, (0, 0, 0, 0))
        canvas = ImageDraw.Draw(img)
        ratio = ((self.x_1 - self.x_0) * 120 / 1080)
        self.child.draw(canvas, self.offset, self.size, ratio)

        return img

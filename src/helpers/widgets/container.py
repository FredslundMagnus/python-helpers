from helpers.colors import Color
from helpers.widgets.size import Size
from helpers.widgets.widget import *


class Container(Widget):
    def __init__(self, color: Color = None, size: Size = None, radius: float = 0.0) -> None:
        self.color = color
        self.size = size
        self.radius = radius
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, ratio: float) -> None:
        dx = offset.dx * ratio
        dy = offset.dy * ratio
        width = self.size.width * ratio
        height = self.size.height * ratio
        if self.color is not None:
            # canvas.rectangle((dx, dy, dx + width, dy + height), fill=self.color.color)
            # canvas.r
            canvas.rounded_rectangle((dx, dy, dx + width, dy + height), radius=self.radius, fill=self.color.color)

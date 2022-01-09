from helpers.colors import Color
from helpers.widgets.widget import *


class Container(Widget):
    def __init__(self, color: Color = None, size: Size = None, radius: float = 0.0, child: Widget = None) -> None:
        self.color = color
        self.size = size
        self.radius = radius
        self.child = child
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        dx = offset.dx * ratio
        dy = offset.dy * ratio
        if self.size is None:
            self.size = max_size

        width = self.size.width * ratio
        height = self.size.height * ratio
        if self.color is not None:
            canvas.rounded_rectangle((dx, dy, dx + width, dy + height), radius=self.radius, fill=self.color.color)
        if self.child is not None:
            self.child.draw(canvas, offset, self.size, ratio)

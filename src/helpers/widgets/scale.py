from helpers.widgets.widget import *


class Scale(Widget):
    def __init__(self, scale: float = 1.0, child: Widget = None) -> None:
        self.scale = scale
        self.child = child
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        if self.child is not None:
            self.child.draw(canvas, offset, max_size, ratio * self.scale)

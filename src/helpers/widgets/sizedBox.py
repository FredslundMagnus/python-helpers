from helpers.widgets.widget import *


class SizedBox(Widget):
    def __init__(self, size: Size = None, child: Widget = None) -> None:
        self.size = size
        self.child = child
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        if self.size is None:
            self.size = max_size

        if self.child is not None:
            self.child.draw(canvas, offset, self.size, ratio)

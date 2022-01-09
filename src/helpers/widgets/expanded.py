from helpers.widgets.widget import *


class Expanded(Widget):
    def __init__(self, flex: float = 1.0, child: Widget = None) -> None:
        self.flex = flex
        self.child = child
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        if self.child is None:
            return
        self.child.draw(canvas, offset, max_size, ratio)

from helpers.widgets.edges import Edges
from helpers.widgets.widget import *


class Padding(Widget):
    def __init__(self, padding: Edges = Edges.zero(), child: Widget = None) -> None:
        self.padding = padding
        self.child = child
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        _offset = Offset(offset.dx + self.padding.left, offset.dy + self.padding.top)
        _size = Size(max_size.width - self.padding.left - self.padding.right, max_size.height - self.padding.top - self.padding.bottom)

        if self.child is not None:
            self.child.draw(canvas, _offset, _size, ratio)

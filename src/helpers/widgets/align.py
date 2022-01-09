from helpers.widgets.alignment import Alignment
from helpers.widgets.widget import *


class Align(Widget):
    def __init__(self, alignment: Alignment = Alignment.center(), child: Widget = None) -> None:
        self.alignment = alignment
        self.child = child
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        if self.child is not None:
            if self.child.size is None:
                raise ValueError("Child needs a size")
            print(self.alignment)
            _offset = Offset(
                offset.dx + (max_size.width - self.child.size.width) * ((self.alignment.x + 1) / 2),
                offset.dy + (max_size.height - self.child.size.height) * ((self.alignment.y + 1) / 2),
            )
            self.child.draw(canvas, _offset, self.child.size, ratio)

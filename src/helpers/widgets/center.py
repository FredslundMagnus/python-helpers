from helpers.widgets.widget import *


class Center(Widget):
    def __init__(self,  child: Widget = None) -> None:
        self.child = child
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        if self.child is not None:
            if self.child.size is None:
                raise ValueError("Child needs a size")
            _offset = Offset(
                offset.dx + (max_size.width - self.child.size.width) * (1/2),
                offset.dy + (max_size.height - self.child.size.height) * (1/2),
            )
            self.child.draw(canvas, _offset, self.child.size, ratio)

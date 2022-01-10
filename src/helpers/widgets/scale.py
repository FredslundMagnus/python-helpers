from helpers.widgets.widget import *


class Scale(Widget):
    def __init__(self, scale: float = 1.0, child: Widget = None) -> None:
        self.scale = scale
        self.child = child
        super().__init__()

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        if self.child is not None:
            _offset = Offset(offset.dx / self.scale, offset.dy / self.scale)
            _size = Size(max_size.width / self.scale, max_size.height / self.scale)
            _ratio = ratio * self.scale
            self.child.draw(canvas, _offset, _size, _ratio)

from __future__ import annotations
from helpers.widgets.widget import *


class Row(Widget):
    def __init__(self, children: list[Widget] = []) -> None:
        self.children = [child for child in children if child is not None]
        super().__init__()

    def drawMin(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        for child in self.children:
            if child.size is None:
                raise ValueError("Child needs a size")
            child.draw(canvas, offset, child.size, ratio)
            offset = Offset(offset.dx + child.size.width, offset.dy)

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        flex_sum = 0
        size_sum = 0
        for child in self.children:
            if child.size is None:
                if child.flex is None or child.flex <= 0:
                    raise ValueError("Child needs a positive flex")
                flex_sum += child.flex
            else:
                size_sum += child.size.width
        if flex_sum == 0:
            self.drawMin(canvas, offset, max_size, ratio)
            return

        rest_width = max_size.width - size_sum

        for child in self.children:
            if child.size is None:
                child.size = Size((child.flex / flex_sum) * rest_width, max_size.height)
            child.draw(canvas, offset, child.size, ratio)
            offset = Offset(offset.dx + child.size.width, offset.dy)

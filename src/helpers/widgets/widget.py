from __future__ import annotations
from helpers.widgets.offset import Offset
from helpers.widgets.size import Size
from PIL.ImageDraw import ImageDraw


class Widget:
    size: Size | None = None
    flex: float | None = None

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        built = self.build(max_size)
        if built is not None:
            built.draw(canvas, offset, max_size, ratio)

    def build(self, size: Size) -> Widget | None:
        return None

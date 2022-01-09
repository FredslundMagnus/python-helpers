from __future__ import annotations
from helpers.widgets.offset import Offset
from helpers.widgets.size import Size
from PIL.ImageDraw import ImageDraw


class Widget:
    size: Size | None = None

    def draw(self, canvas: ImageDraw, offset: Offset, max_size: Size, ratio: float) -> None:
        pass

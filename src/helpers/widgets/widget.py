from helpers.widgets.offset import Offset
from PIL.ImageDraw import ImageDraw


class Widget:
    def draw(self, canvas: ImageDraw, offset: Offset, ratio: float) -> None:
        pass

from helpers.colors import Color
from helpers.widgets.size import Size
from helpers.widgets.widget import Widget


class Container(Widget):
    def __init__(self, color: Color, size: Size) -> None:
        self.color = color
        self.size = size
        super().__init__()

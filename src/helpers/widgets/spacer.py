from helpers.widgets.widget import *


class Spacer(Widget):
    def __init__(self, flex: float = 1.0) -> None:
        self.flex = flex
        super().__init__()

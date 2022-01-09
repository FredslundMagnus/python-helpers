from helpers.widgets.widget import Widget


class Root(Widget):
    def __init__(self, x_0: float, y_0: float, x_1: float, y_1: float, child: Widget) -> None:
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1
        self.width = (x_1-x_0) * 100
        self.height = (y_1-y_0) * 100
        self.child = child
        super().__init__()

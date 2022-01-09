from __future__ import annotations
from helpers.colors import Colors
from helpers.widgets.sizedBox import SizedBox
from helpers.widgets.widget import *
from helpers.widgets.column import Column
from helpers.widgets.container import Container


class FileEditor(Widget):
    def __init__(self, filename: str | None = None) -> None:
        self.filename = filename
        super().__init__()

    def build(self, size: Size) -> Widget | None:
        return Column(
            children=[
                Container(
                    color=Colors.red,
                    size=Size(size.width, 20),
                ),
            ],
        )

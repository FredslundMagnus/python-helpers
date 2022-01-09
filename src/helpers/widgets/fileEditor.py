from __future__ import annotations
from helpers.colors import Colors
from helpers.widgets.padding import Padding
from helpers.widgets.sizedBox import SizedBox
from helpers.widgets.widget import *
from helpers.widgets.column import Column
from helpers.widgets.container import Container
from helpers.widgets.expanded import Expanded
from helpers.widgets.edges import Edges
from helpers.widgets.row import Row


class FileEditor(Widget):
    def __init__(self, filename: str | None = None) -> None:
        self.filename = filename
        super().__init__()

    def build(self, size: Size) -> Widget | None:
        return Column(
            children=[
                Container(
                    color=Colors.red,
                    size=Size(size.width, 32),
                    child=Padding(
                        padding=Edges.all(12),
                        child=Row(
                            Container(size=Size(8, 8), color=Colors.red, radius=4),
                            SizedBox(size=Size(8, 8)),
                            Container(size=Size(8, 8), color=Colors.yellow, radius=4),
                            SizedBox(size=Size(8, 8)),
                            Container(size=Size(8, 8), color=Colors.green, radius=4),
                            SizedBox(size=Size(24, 8)),
                        ),
                    ),
                ),
                Expanded(
                    child=Container(
                        color=Colors.green,
                        child=Padding(
                            padding=Edges.all(10),
                            child=Container(
                                color=Colors.blue,
                            )
                        )
                    ),
                ),
            ],
        )

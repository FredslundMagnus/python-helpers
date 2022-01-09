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
                SizedBox(
                    size=Size(size.width, 36),
                    child=Padding(
                        padding=Edges.all(10),
                        child=Row(
                            children=[
                                Container(size=Size(16, 16), color=Colors.red, radius=6),
                                SizedBox(size=Size(8, 16)),
                                Container(size=Size(16, 16), color=Colors.yellow, radius=6),
                                SizedBox(size=Size(8, 16)),
                                Container(size=Size(16, 16), color=Colors.green, radius=6),
                                SizedBox(size=Size(24, 16)),
                                # self.filename if self.filename is not None else None,
                            ],
                        ),
                    ),
                ),
                Expanded(
                    child=Padding(
                        padding=Edges.all(10),
                        child=Container(
                            color=Colors.gray.c700,
                        ),
                    ),
                ),
            ],
        )

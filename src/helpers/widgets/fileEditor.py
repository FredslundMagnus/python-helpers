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
from helpers.widgets.text import Text
from helpers.widgets.center import Center


class FileEditor(Widget):
    def __init__(self, filename: str | None = None, child: Widget | None = None) -> None:
        self.filename = filename
        self.child = child
        super().__init__()

    def build(self, size: Size) -> Widget | None:
        return Column(
            children=[
                SizedBox(
                    size=Size(size.width, 46),
                    child=Padding(
                        padding=Edges.all(16),
                        child=Row(
                            children=[
                                Container(size=Size(14, 14), color=Colors.red, radius=7),
                                SizedBox(size=Size(8, 14)),
                                Container(size=Size(14, 14), color=Colors.yellow, radius=7),
                                SizedBox(size=Size(8, 14)),
                                Container(size=Size(14, 14), color=Colors.green, radius=7),
                                Expanded(child=Center(child=Text(self.filename, fontSize=14.0))) if self.filename is not None else None,
                                SizedBox(size=Size(14+8+14+8+14, 14)),
                            ],
                        ),
                    ),
                ),
                Expanded(
                    child=Padding(
                        padding=Edges.all(16),
                        child=self.child,
                    ),
                ),
            ],
        )

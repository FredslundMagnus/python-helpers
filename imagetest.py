from __future__ import annotations
from src.helpers.colors import Color, Colors
from src.helpers.render import Background, render_image, render_video
from src.helpers.widgets.widgets import *
from time import time


children = [
    FileEditor(
        filename="example.py",
        child=Code.fromFile(
            "main.py",
            fontSize=float("inf"),
            functions={"dtu", "set", "get"},
            classes={"Parameters", "Database", "Colors"},
            notModules={"database"}
        ),
    ),
    FileEditor(
        filename="Terminal",
        child=Console(
            """C:\\Python> python example.py
Hello World!

C:\\Python>""",
            fitLines=24,
        ),
    ),
    FileEditor(filename="short_name.py"),
]

test0 = [Background(color=Colors.blue, boxes=[(1, 1, 5, 8), (6, 1, 10, 8), (11, 1, 15, 8)], children=children) for _ in range(40)]

test1 = Background.transition(
    Background(color=Colors.blue, boxes=[(1, 1, 5, 8), (6, 1, 10, 8), (11, 1, 15, 8)]),
    Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8), (17, 1, 30, 8)]),
    frames=40,
    children=children,
)

test2 = [Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)], children=children) for _ in range(40)]

test3 = Background.transition(
    Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)]),
    Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 30, 8)]),
    frames=40,
    children=children,
)

test4 = [Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8)], children=children) for _ in range(40)]

test5 = Background.transition(
    Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 30, 8)]),
    Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)]),
    frames=40,
)

example1 = test1 + test2 + test3 + test4 + test5


def ani6(animation: float) -> list[Widget]:
    start, end = 0.5, 1.0
    scale = start + (end-start)*animation
    return [Scale(scale=scale, child=child) for child in children]


def box(center_x: float = 8.0, center_y: float = 4.5, ratio: float = 16/9, height: float | None = None, width: float | None = None) -> tuple(float, float, float, float):
    if height is None:
        height = width/ratio
    if width is None:
        width = height*ratio
    h_height, h_width = height/2, width/2
    return (center_x-h_width, center_y-h_height, center_x+h_width, center_y+h_height)


test6 = Background.transition(
    Background(color=Colors.blue, boxes=[box(height=3.5, center_x=8.0-4.0+16/9/4), box(height=3.5, center_x=8.0+4.0-16/9/4)]),
    Background(color=Colors.blue, boxes=[box(height=7.0), box(height=7.0, center_x=8.0+16.0)]),
    frames=40,
    children=ani6,
)

test7 = Background.transition(
    Background(color=Colors.blue, boxes=[box(height=3.5, center_x=8.0-4.0+16/9/4), box(height=3.5, center_x=8.0+4.0-16/9/4)]),
    Background(color=Colors.blue, boxes=[box(height=7.0, center_x=8.0-16.0), box(height=7.0)]),
    frames=40,
    children=ani6,
)

test8 = Background(color=Colors.green, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.gray.c900)], children=children)
test9 = Background(color=Colors.green, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.black)], children=children)


def test10(color): return Background.transition(
    Background(color=color, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.gray.c900)]),
    Background(color=color, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 21, 8, Colors.gray.c900)]),
    frames=40,
    children=children,
)


def small(color): return [Background(color=color, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.gray.c900)], children=children) for _ in range(40)]
def big(color): return [Background(color=color, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 21, 8, Colors.gray.c900)], children=children) for _ in range(40)]


def textConsoleSplit(color: Color) -> Background:
    return Background(color=color, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.gray.c900)], children=children)


def example(color: Color):
    return (big(color) + list(reversed(test10(color))) + small(color) + test10(color))*3


test: bool = False
size = (3840, 2160)
idea = list(reversed(test6)) + test7 + list(reversed(test7)) + test6


render_image("green", textConsoleSplit(Colors.green), size=size, test=test)
render_image("blue", textConsoleSplit(Colors.blue), size=size, test=test)
render_image("brown", textConsoleSplit(Colors.brown), size=size, test=test)
render_image("deepOrange", textConsoleSplit(Colors.deepOrange), size=size, test=test)
render_image("red", textConsoleSplit(Colors.red), size=size, test=test)

render_video("green", example(Colors.green), size=size, test=test)
render_video("blue", example(Colors.blue), size=size, test=test)
render_video("brown", example(Colors.brown), size=size, test=test)
render_video("deepOrange", example(Colors.deepOrange), size=size, test=test)
render_video("red", example(Colors.red), size=size, test=test)

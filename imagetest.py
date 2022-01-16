from __future__ import annotations
from src.helpers.colors import Color, Colors
from src.helpers.render import Background, render_image, render_video
from src.helpers.widgets.widgets import *
from time import time


def flip(l: list[Background]) -> list[Background]:
    return list(reversed(l))


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

example1 = test1 + test2 + test3 + test4


def ani6(animation: float) -> list[Widget]:
    start, end = 0.5, 1.0
    scale = start + (end-start)*animation
    return [Scale(scale=scale, child=child) for child in children]


def box(center_x: float = 8.0, center_y: float = 4.5, ratio: float = 16/9, height: float | None = None, width: float | None = None, color: Color | None = None) -> tuple[float, float, float, float] | tuple[float, float, float, float, Color]:
    if height is None:
        height = width/ratio
    if width is None:
        width = height*ratio
    h_height, h_width = height/2, width/2
    if color is None:
        return (center_x-h_width, center_y-h_height, center_x+h_width, center_y+h_height)
    return (center_x-h_width, center_y-h_height, center_x+h_width, center_y+h_height, color)


def scaleAni(color: Color) -> list[Background]:
    tmp1 = Background.transition(
        Background(color=color, boxes=[box(height=3.5, center_x=8.0-4.0+16/9/4), box(height=3.5, center_x=8.0+4.0-16/9/4, color=Colors.gray.c900)]),
        Background(color=color, boxes=[box(height=7.0), box(height=7.0, center_x=8.0+16.0, color=Colors.gray.c900)]),
        frames=40,
        children=ani6,
    )

    tmp2 = Background.transition(
        Background(color=color, boxes=[box(height=3.5, center_x=8.0-4.0+16/9/4), box(height=3.5, center_x=8.0+4.0-16/9/4, color=Colors.gray.c900)]),
        Background(color=color, boxes=[box(height=7.0, center_x=8.0-16.0), box(height=7.0, color=Colors.gray.c900)]),
        frames=40,
        children=ani6,
    )

    tmp5 = [Background(
        color=color,
        boxes=[box(height=3.5, center_x=8.0-4.0+16/9/4), box(height=3.5, center_x=8.0+4.0-16/9/4, color=Colors.gray.c900)],
        children=[Scale(scale=0.5, child=child) for child in children]
    ) for _ in range(40)]

    tmp3 = [Background(color=color, boxes=[box(height=7.0)], children=children[0:1]) for _ in range(40)]
    tmp4 = [Background(color=color, boxes=[box(height=7.0, color=Colors.gray.c900)], children=children[1:2]) for _ in range(40)]

    return (tmp3 + flip(tmp1) + tmp5 + tmp2 + tmp4 + flip(tmp2) + tmp5 + tmp1) * 2


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
colors = [
    ("green", Colors.green),
    ("blue", Colors.blue),
    ("brown", Colors.brown),
    ("deepOrange", Colors.deepOrange),
    ("red", Colors.red),
    ("indigo", Colors.indigo),
    ("pink", Colors.pink),
]

# for name, color in colors:
#     render_image(name, textConsoleSplit(color), size=size, test=test)

# for name, color in colors:
#     render_video(name, example(color), size=size, test=test)

for name, color in colors:
    render_video(name + "Scale", scaleAni(color), size=size, test=test)

from __future__ import annotations
import cv2
from src.helpers.curves import Curves
from src.helpers.colors import Colors
from src.helpers.image.background import Background
from src.helpers.widgets.widgets import *
from PIL import Image
import numpy as np


def make(name: str, files: list[Background], fps: int = 60, size: tuple[int, int] = (1920, 1080)):
    video = cv2.VideoWriter(f'Videos/{name}.mov', 4, fps, size)

    for image in files:
        image.load(size=size)
        background = Image.open(image.name(size=size))
        for img in (root.draw(size=size) for root in image.children):
            background.paste(img, (0, 0), img)

        pil_image = np.array(background.convert('RGB'))
        open_cv_image = pil_image[:, :, ::-1].copy()
        video.write(open_cv_image)

    cv2.destroyAllWindows()
    video.release()


# Background(color=Colors.brown, boxes=[(0, 0, 16, 9)]).load(size=(1920, 1080))

# Background(color=Colors.brown, boxes=[(16/9, 1, 16-16/9, 8)]).load(size=(1920, 1080))

# Background(color=Colors.brown, boxes=[(1, 1, 7.5, 8, Colors.green), (8.5, 1, 15, 8, Colors.red)]).load(size=(1920, 1080))

# Background(color=Colors.brown, boxes=[(1, 1, 7.5, 8, Colors.blue), (8.5, 1, 15, 8)]).load(size=(1920, 1080))

# Background(color=Colors.brown, boxes=[(1, 1, 5, 8, Colors.blue), (6, 1, 10, 8), (11, 1, 15, 8, Colors.green)]).load(size=(1920, 1080))

# trans = Background.transition(
#     Background(color=Colors.brown, boxes=[(1, 1, 5, 8, Colors.blue), (6, 1, 10, 8), (11, 1, 15, 8, Colors.green)]),
#     Background(color=Colors.yellow, boxes=[(1, 1, 5, 8, Colors.green), (6, 1, 10, 8, Colors.red), (11, 1, 15, 8)]),
#     frames=10,
#     curve=Curves.linear,
# )

# trans2 = Background.transition(
#     Background(color=Colors.brown, boxes=[(1, 1, 5, 8, Colors.blue), (6, 1, 10, 8), (11, 1, 15, 8, Colors.green)]),
#     Background(color=Colors.yellow, boxes=[(1, 1, 7.5, 8, Colors.green), (8.5, 1, 15, 8, Colors.red), (17, 1, 30, 8)]),
#     frames=40,
#     curve=Curves.linear,
# )

test0 = [Background(color=Colors.blue, boxes=[(1, 1, 5, 8), (6, 1, 10, 8), (11, 1, 15, 8)], children=[
    Container(
        color=Colors.red,
        child=Container(
            color=Colors.green,
            size=Size(100, 100),
            radius=10,
        ),
    ),
    Container(
        color=Colors.yellow,
        child=Padding(
            padding=Edges.all(10.0),
            child=Container(
                color=Colors.blue,
                child=Align(
                    alignment=Alignment.centerRight,
                    child=Container(
                        color=Colors.green,
                        size=Size(200, 100),
                    ),
                ),
            ),
        ),
    ),
    Container(
        color=Colors.yellow,
        child=Row(
            children=[
                Container(
                    color=Colors.purple,
                    size=Size(100, 200),
                    radius=30,
                ),
                Container(
                    color=Colors.purple,
                    size=Size(100, 200),
                    radius=30,
                ),
            ],
        ),
    ),
]) for _ in range(40)]

test1 = Background.transition(
    Background(color=Colors.blue, boxes=[(1, 1, 5, 8), (6, 1, 10, 8), (11, 1, 15, 8)]),
    Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8), (17, 1, 30, 8)]),
    frames=40,
    curve=Curves.easeInOut,
)

test2 = [Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)]) for _ in range(40)]

test3 = Background.transition(
    Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)]),
    Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 30, 8)]),
    frames=40,
    curve=Curves.easeInOut,
)

test4 = [Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8)]) for _ in range(40)]

# test5 = Background.transition(
#     Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 30, 8)]),
#     Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)]),
#     frames=40,
#     curve=Curves.easeInOut,
# )


# make("eksempelHD2", (test0 + test1 + test2 + test3 + test4 + list(reversed(test3)) + test2 + list(reversed(test1))) * 3, size=(1920, 1080))
make("testContainer", test0, size=(1920, 1080))
# [tran.load() for tran in trans]
# [tran.load() for tran in trans2]


# make("test", trans, fps=5)
# make("test2", trans2, fps=5)

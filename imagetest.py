from __future__ import annotations
import cv2
from src.helpers.curves import Curves
from src.helpers.colors import Color, Colors
from src.helpers.image.background import Background
from src.helpers.widgets.widgets import *
from PIL import Image
import numpy as np
from enum import Enum


class VideoFormat(Enum):
    mov = 4
    avi = 0


def create_video(name: str, files: list[Background], fps: int = 60, size: tuple[int, int] = (1920, 1080), test: bool = False, videoFormat: VideoFormat = VideoFormat.mov):
    video = cv2.VideoWriter(f'Videos/{name}.{videoFormat.name.split(".")[-1]}', videoFormat.value, fps, size)

    for i, image in enumerate(files, start=1):
        print(f"{i} out of {len(files)}")
        if not test:
            image.load(size=size)
        background = Image.new(mode="RGBA", size=size, color=(*image.color.color, 255)) if test else Image.open(image.name(size=size))
        for img in (root.draw(size=size, test=test) for root in image.children):
            background.paste(img, (0, 0), img)

        pil_image = np.array(background.convert('RGB'))
        open_cv_image = pil_image[:, :, ::-1].copy()
        video.write(open_cv_image)

    cv2.destroyAllWindows()
    video.release()


def create_image(name: str, file: Background, size: tuple[int, int] = (1920, 1080), test: bool = False):
    if not test:
        file.load(size=size)
    background = Image.new(mode="RGBA", size=size, color=(*file.color.color, 255)) if test else Image.open(file.name(size=size))
    for img in (root.draw(size=size, test=test) for root in file.children):
        background.paste(img, (0, 0), img)
    background.save(f"Images/{name}.png")


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
    curve=Curves.easeInOut,
    children=children,
)

test2 = [Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)], children=children) for _ in range(40)]

test3 = Background.transition(
    Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)]),
    Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 30, 8)]),
    frames=40,
    curve=Curves.easeInOut,
    children=children,
)

test4 = [Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8)], children=children) for _ in range(40)]

# test5 = Background.transition(
#     Background(color=Colors.blue, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 30, 8)]),
#     Background(color=Colors.blue, boxes=[(1, 1, 7.5, 8), (8.5, 1, 15, 8)]),
#     frames=40,
#     curve=Curves.easeInOut,
# )


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
    curve=Curves.easeInOut,
    children=ani6,
)

test7 = Background.transition(
    Background(color=Colors.blue, boxes=[box(height=3.5, center_x=8.0-4.0+16/9/4), box(height=3.5, center_x=8.0+4.0-16/9/4)]),
    Background(color=Colors.blue, boxes=[box(height=7.0, center_x=8.0-16.0), box(height=7.0)]),
    frames=40,
    curve=Curves.easeInOut,
    children=ani6,
)

test8 = Background(color=Colors.green, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.gray.c900)], children=children)
test9 = Background(color=Colors.green, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.black)], children=children)


def test10(color): return Background.transition(
    Background(color=color, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.gray.c900)]),
    Background(color=color, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 21, 8, Colors.gray.c900)]),
    frames=40,
    curve=Curves.easeInOut,
    children=children,
)


def small(color): return [Background(color=color, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.gray.c900)], children=children) for _ in range(40)]
def big(color): return [Background(color=color, boxes=[(16/9, 1, 16-16/9, 8), (17, 1, 21, 8, Colors.gray.c900)], children=children) for _ in range(40)]


test: bool = False
idea = list(reversed(test6)) + test7 + list(reversed(test7)) + test6


def textConsoleSplit(color: Color) -> Background:
    return Background(color=color, boxes=[(1, 1, 10, 8), (11, 1, 15, 8, Colors.gray.c900)], children=children)


if test:
    # create_video("testHD", test0[:20], size=(1920*2, 1080*2), test=test)
    # create_image("test0Container", test0[0], size=(1920*2, 1080*2), test=test)
    # create_video("test6HD", idea, size=(1920*2, 1080*2), test=test)
    create_video("textAndConsole4kTest", (big(Colors.green) + list(reversed(test10(Colors.green))) + small(Colors.green) + test10(Colors.green))*3, size=(1920*2, 1080*2), test=test)

else:
    # create_image("testLang", test4[0], size=(1920*2, 1080*2), test=test)
    # create_image("withConsole1", test8, size=(1920*2, 1080*2), test=test)
    # create_image("withConsole2", test9, size=(1920*2, 1080*2), test=test)
    # create_image("redTextConsole", textConsoleSplit(Colors.red), size=(1920*2, 1080*2), test=test)
    # create_image("deepOrangeTextConsole", textConsoleSplit(Colors.deepOrange), size=(1920*2, 1080*2), test=test)
    # create_image("orangeTextConsole", textConsoleSplit(Colors.orange), size=(1920*2, 1080*2), test=test)
    create_image("yellowTextConsole", textConsoleSplit(Colors.yellow), size=(1920*2, 1080*2), test=test)
    # create_image("brownTextConsole", textConsoleSplit(Colors.brown), size=(1920*2, 1080*2), test=test)
    create_video("textAndConsole4kNewGreen", (big(Colors.green) + list(reversed(test10(Colors.green))) + small(Colors.green) + test10(Colors.green))*3, size=(1920*2, 1080*2), test=test)
    create_video("textAndConsole4kNewRed", (big(Colors.red) + list(reversed(test10(Colors.red))) + small(Colors.red) + test10(Colors.red))*3, size=(1920, 1080), test=test)
    # create_video("test6HD4", idea, size=(1920, 1080), test=test, fps=30)
    # create_video("test4k", (test0 + test1 + test2 + test3 + test4 + list(reversed(test3)) + test2 + list(reversed(test1))) * 3, size=(1920*2, 1080*2))
    # create_image("test0Container", test0[0], size=(1920*2, 1080*2))
    # create_image("test1Container", test2[0], size=(1920*2, 1080*2))
    # create_image("test2Container", test4[0], size=(1920*2, 1080*2))
# create_image("test0ContainerSmall", test0[0], size=(1920, 1080))
# create_image("test1ContainerSmall", test2[0], size=(1920, 1080))
# create_image("test2ContainerSmall", test4[0], size=(1920, 1080))
# [tran.load() for tran in trans]
# [tran.load() for tran in trans2]


# make("test", trans, fps=5)
# make("test2", trans2, fps=5)

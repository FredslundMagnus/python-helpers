from __future__ import annotations
import cv2
from src.helpers.curves import Curves
from src.helpers.colors import Colors
from src.helpers.image.background import Background
from src.helpers.widgets.widgets import *
from PIL import Image
import numpy as np


def create_video(name: str, files: list[Background], fps: int = 60, size: tuple[int, int] = (1920, 1080), test: bool = False):
    video = cv2.VideoWriter(f'Videos/{name}.mov', 4, fps, size)

    for i, image in enumerate(files, start=1):
        print(f"{i} out of {len(files)}")
        if not test:
            image.load(size=size)
        background = Image.new(mode="RGBA", size=size, color=(*image.color.color, 0)) if test else Image.open(image.name(size=size))
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
    background = Image.new(mode="RGBA", size=size, color=(*file.color.color, 0)) if test else Image.open(file.name(size=size))
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
    FileEditor(filename="example_of_filename.py"),
    FileEditor(filename="another_great_but_long_name.py"),
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

test: bool = True

if test:
    create_video("testHD", test0[:20], size=(1920*2, 1080*2), test=test)
    create_image("test0Container", test0[0], size=(1920*2, 1080*2), test=test)
else:
    create_video("testHD", (test0 + test1 + test2 + test3 + test4 + list(reversed(test3)) + test2 + list(reversed(test1))) * 3, size=(1920*2, 1080*2))
    create_image("test0Container", test0[0], size=(1920*2, 1080*2))
    create_image("test1Container", test2[0], size=(1920*2, 1080*2))
    create_image("test2Container", test4[0], size=(1920*2, 1080*2))
# create_image("test0ContainerSmall", test0[0], size=(1920, 1080))
# create_image("test1ContainerSmall", test2[0], size=(1920, 1080))
# create_image("test2ContainerSmall", test4[0], size=(1920, 1080))
# [tran.load() for tran in trans]
# [tran.load() for tran in trans2]


# make("test", trans, fps=5)
# make("test2", trans2, fps=5)

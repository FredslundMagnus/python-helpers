from __future__ import annotations
from vapory.vapory import *
from helpers.colors import Color, Colors
from PIL import Image as IMG
from os.path import join, exists


def colorize(color: Color) -> Texture:
    return Texture(Pigment('color', [v/255 for v in color.color]))


class Item:
    def __str__(self):
        return str(self.item)


class BackGroundBox(Item):
    def __init__(self, color: Color, distance: float) -> None:
        self.item = Box([100, 100, distance+0.1], [-100, -100, distance], colorize(color))


class Background:
    def __init__(self, color: Color, boxes: list[tuple[float, float, float, float]] = [], box_color: Color = Colors.gray.c800, folder: str = "backgrounds") -> None:
        self.folder = folder
        self.color_name = str(color.color)[1: -1].replace(', ', '_')
        self.box_color_name = str(box_color.color)[1: -1].replace(', ', '_')
        self.box_color = box_color
        self.boxes_shape = boxes
        self.scene = Scene(
            Camera('location', [0, 0, -6], 'look_at',  [0, 0, 0]),
            [
                LightSource([2, 4, -3], 'color', [1.5, 1.5, 1.5], 'area_light <5, 0, 0>, <0, 5, 0>, 5, 5', 'adaptive 2 area_illumination on', 'jitter'),
                BackGroundBox(color=color, distance=2),
                # Box([16/3, 9/3, 1.9], [-16/3, -9/3, 1.8], colorize(Colors.gray.c800))
                *self.boxes
            ]
        )

    @property
    def boxes(self) -> list[Box]:
        return [Box([b[2], -b[3], 1.9], [b[0], b[1], 1.8], colorize(self.box_color)) for b in self.boxes_shape]

    def transform(pos: float) -> float:
        return pos

    def render(self, antialiasing: float = 0.001, quality: int = 11, size: tuple[int, int] = (1920, 1080)) -> None:
        width, height = size
        self.file_name = join(self.folder, f"background-{self.color_name}-{width}-{height}.png")
        self.scene.render(outfile=self.file_name, width=width, height=height, quality=quality, antialiasing=antialiasing)

    def load(self, size: tuple[int, int] = (1920, 1080)):
        width, height = size
        self.file_name = join(self.folder, f"background-{self.color_name}-{width}-{height}.png")
        if not exists(self.file_name):
            self.render()
        return IMG.open(self.file_name)

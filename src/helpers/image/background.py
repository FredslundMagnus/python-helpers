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
    def __init__(self, color: Color, boxes: list[tuple[float, float, float, float] | tuple[float, float, float, float, Color]] = [], box_color: Color = Colors.gray.c800, folder: str = "backgrounds") -> None:
        self.folder = folder
        self.color_name = str(color.color)[1: -1].replace(', ', '_')
        self.box_color_name = str(box_color.color)[1: -1].replace(', ', '_')
        self.boxes_shape = [(tuple(list(b) + [box_color]) if len(b) == 4 else b) for b in boxes]
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
        return [Box([self.fix(b[2]), self.fix(-b[3], x=False), 1.9], [self.fix(b[0]), self.fix(-b[1], x=False), 1.8], colorize(b[4])) for b in self.boxes_shape]

    @property
    def boxes_name(self) -> list[Box]:
        return "_".join([f"{self.fix(b[0])}-{self.fix(b[1])}-{self.fix(b[2])}-{self.fix(b[3])}-" + str(b[4].color)[1: -1].replace(', ', '_') for b in self.boxes_shape])

    def fix(self, pos: float, x: bool = True) -> float:
        b = -6.94 if x else 3.9
        a = 0.867
        return int((a*pos + b) * 10000) / 10000

    def name(self, size: tuple[int, int] = (1920, 1080)) -> str:
        width, height = size
        return join(self.folder, f"background-{self.color_name}-{width}-{height}-{self.boxes_name}.png")

    def render(self, antialiasing: float = 0.001, quality: int = 11, size: tuple[int, int] = (1920, 1080)) -> None:
        width, height = size
        self.scene.render(outfile=self.name(size), width=width, height=height, quality=quality, antialiasing=antialiasing)

    def load(self, size: tuple[int, int] = (1920, 1080)):
        name = self.name(size)
        if not exists(name):
            self.render()
        return IMG.open(name)

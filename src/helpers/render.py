from __future__ import annotations
from PIL import Image, ImageDraw, ImageFilter
from helpers.colors import Colors, Color
from helpers.widgets.widget import Widget
from helpers.widgets.root import Root
from helpers.curves import Curve, Curves
from helpers.files import makeSureFolderExists
import numpy as np
from numba import njit
from time import time
from os.path import join, exists
from functools import lru_cache  # python 3.9 has cache wich is faster for maxsize=None
from PIL import Image
import numpy as np
from enum import Enum
import cv2
from os import mkdir

name = "your_file.png"
intencity = 0.9
u_Shininess = 10.0
u_Light_position = np.array([16/9*2.3, -0.5*5, 2*8])
# print(u_Light_position)
camera = np.array([0.5, 0.5, 2])
# size = (3840, 2160)
blur = 8
factor = None
# background = Colors.red
# box1: tuple[float, float, float, float, Color] = (1.0, 1.0, 10.0, 8.0, Colors.gray.c800)
# box2: tuple[float, float, float, float, Color] = (11.0, 1.0, 15.0, 8.0, Colors.gray.c900)
# boxes: list[tuple[float, float, float, float, Color]] = [box1, box2]


class Background:
    def __init__(self, color: Color, boxes: list[tuple[float, float, float, float] | tuple[float, float, float, float, Color]] = [], box_color: Color = Colors.gray.c800, folder: str = "Background", save_together: bool = False, children: list[Widget] = []) -> None:
        self.folder = folder
        self.color = color
        self.save_together = save_together
        self.color_name = str(self.color.color)[1: -1].replace(', ', '_')
        self.boxes: list[tuple[float, float, float, float, Color]] = [(tuple(list(b) + [box_color]) if len(b) == 4 else b) for b in boxes]
        self.children = [Root(*box[:4], child) for child, box in zip(children, boxes)]

    @property
    def boxes_name(self) -> list[str]:
        return "_".join([f"{self.fix(b[0])}-{self.fix(b[1])}-{self.fix(b[2])}-{self.fix(b[3])}-" + str(b[4].color)[1: -1].replace(', ', '_') for b in self.boxes])

    def fix(self, pos: float, x: bool = True) -> float:
        b = -6.94 if x else 3.9
        a = 0.867
        return int((a*pos + b) * 10000) / 10000

    def name(self, size: tuple[int, int] = (1920, 1080)) -> str:
        width, height = size
        return join(makeSureFolderExists(self.folder, gitignore=True), f"full-{self.color_name}-{width}-{height}-{self.boxes_name}.png")

    def empty_name(self, size: tuple[int, int] = (1920, 1080)) -> str:
        width, height = size
        return join(makeSureFolderExists("Colors", gitignore=True), f"color-{width}-{height}-{self.color_name}.png")

    def rendered_boxes_name(self, size: tuple[int, int] = (1920, 1080)) -> str:
        width, height = size
        return join(makeSureFolderExists("Boxes", gitignore=True), f"boxes-{width}-{height}-{self.boxes_name}.png")

    def render(self, size: tuple[int, int] = (1920, 1080)) -> None:
        empty_name = self.empty_name(size)
        if not exists(empty_name):
            im = Image.new("RGBA", size)
            canvas = ImageDraw.Draw(im)

            drawBackground(canvas, self.color, size)

            im.save(empty_name)
        else:
            im = Image.open(empty_name)

        boxes_name = self.rendered_boxes_name(size)
        if not exists(boxes_name):
            im2 = Image.new("RGBA", size)
            canvas2 = ImageDraw.Draw(im2)

            for box in self.boxes:
                drawBoxShadow(im2, box, size)

            for box in self.boxes:
                drawBoxBorder(canvas2, box)

            for box in self.boxes:
                drawBox(canvas2, box, size)

            im2.save(boxes_name)
        else:
            im2 = Image.open(boxes_name)

        im.alpha_composite(im2, (0, 0))
        if self.save_together:
            im.save(self.name(size))
        return im

    def load(self, size: tuple[int, int] = (1920, 1080)):
        global factor
        factor = size[0] / 16
        if self.save_together:
            name = self.name(size)
            if not exists(name):
                return self.render(size=size)
            return Image.open(name)
        else:
            return self.render(size=size)

    @staticmethod
    def transition(background1: Background, background2: Background, frames: int, curve: Curve = Curves.easeInOut, children: list[Widget] = []) -> list[Background]:
        backgrounds: list[Background] = []
        for step in (curve(i/(frames-1)) for i in range(frames)):
            boxes: list[tuple[float, float, float, float, Color]] = []
            for box1, box2, in zip(background1.boxes, background2.boxes):
                *vs1, c1 = box1
                *vs2, c2 = box2
                box = tuple([(v2-v1)*step + v1 for v1, v2 in zip(vs1, vs2)] + [Colors.interpolate(c1, c2, step)])
                boxes.append(box)
            color = Colors.interpolate(background1.color, background2.color, step)
            try:
                _children = children(step)
            except Exception:
                _children = children
            backgrounds.append(Background(color=color, boxes=boxes, children=_children))
        return backgrounds


@njit
def normalize(v):
    return v / np.sqrt(np.sum(v**2))


@lru_cache(maxsize=None)
@njit
def calculate_highlight(x: float, y: float, z: float) -> tuple[float, float, float]:
    # Calculate a vector from the fragment location to the light source
    v_Vertex = np.array([x, y, z])
    v_Normal = np.array([0, 0, 1])

    to_light = u_Light_position - v_Vertex
    to_light = normalize(to_light)

    # The vertex's normal vector is being interpolated across the primitive
    # which can make it un-normalized. So normalize the vertex's normal vector.
    vertex_normal = normalize(v_Normal)

    # Calculate the reflection vector
    reflection = 2.0 * np.dot(vertex_normal, to_light) * vertex_normal - to_light

    # Calculate a vector from the fragment location to the camera.
    # The camera is at the origin, so negating the vertex location gives the vector
    to_camera = camera - v_Vertex

    # Calculate the cosine of the angle between the reflection vector
    # and the vector going to the camera.
    reflection = normalize(reflection)
    to_camera = normalize(to_camera)
    cos_angle = np.dot(reflection, to_camera)
    if cos_angle < 0.0:
        cos_angle = 0.0
    if cos_angle > 1.0:
        cos_angle = 1.0
    # cos_angle = np.clip(cos_angle, 0.0, 1.0)
    cos_angle = pow(cos_angle, u_Shininess)

    #   // If this fragment gets a specular reflection, use the light's color,
    #   // otherwise use the objects's color
    #   specular_color = u_Light_color * cos_angle;
    #   object_color = vec3(v_Color) * (1.0 - cos_angle);
    #   color = specular_color + object_color;
    return cos_angle
    # return Color.interpolate(color, Colors.white,  cos_angle).color


@njit
def _interpolate(pixel_color: tuple[int, int, int], value: float) -> tuple[int, int, int]:
    return [int(p*(0.1 + 0.9*value)) for p in pixel_color]
    # return tuple(int((v2 - v1)*x+v1) for v1, v2 in zip(color1, color2))


@njit
def fixScale(v: int, size: tuple[int, int]) -> float:
    return v / (size[1] - 1)


def drawBackground(canvas: ImageDraw.ImageDraw, pixel_color: Color, size: tuple[int, int]):
    z = -2.0
    for y in range(size[1]):
        _y = fixScale(y, size)
        for x in range(size[0]):
            _x = fixScale(x, size)
            cos_angle = calculate_highlight(_x, _y, z)
            # color = Color.interpolate(Color.interpolate(pixel_color, Colors.black, 0.9), pixel_color,  cos_angle*intencity).color
            # color = getColor(pixel_color.color, cos_angle*intencity)
            # color = Color.interpolate(Colors.black, pixel_color,  cos_angle*intencity*0.9+0.1).color
            color = _interpolate(pixel_color.color, cos_angle*intencity)
            canvas.point((x, y), (*color, 255))


def drawBox(canvas: ImageDraw.ImageDraw, box: tuple[float, float, float, float, Color], size: tuple[int, int]) -> None:
    z = -1.9
    pixel_color = box[4]
    for y in range(size[1]):
        _y = fixScale(y, size)
        for x in range(size[0]):
            if not (factor * box[0] < x < factor * box[2] and factor * box[1] < y < factor * box[3]):
                continue
            _x = fixScale(x, size)
            cos_angle = calculate_highlight(_x, _y, z)
            # color = Color.interpolate(Color.interpolate(pixel_color, Colors.black, 0.9), pixel_color,  cos_angle*intencity).color
            color = _interpolate(pixel_color.color, cos_angle*intencity)
            canvas.point((x, y), (*color, 255))


@njit
def fixX(x: float) -> float:
    return (x-14)*1.015 + 14


@njit
def fixY(y: float) -> float:
    return (y-0)*1.02 + 0.07


@njit
def centerX(x: float) -> float:
    return (x-8)*0.988 + 8


@njit
def centerY(y: float) -> float:
    return (y-4.5)*0.988 + 4.5


@njit
def colorX(x: float) -> float:
    return abs(x-14)/9/2


@njit
def colorY(y: float) -> float:
    return abs(y-0)/9/2


def edgeShadow(canvas: ImageDraw.ImageDraw, corner1: tuple[float, float], corner2: tuple[float, float], color: tuple[int, int, int, int]) -> None:
    canvas.polygon((
        factor * fixX(corner1[0]), factor * fixY(corner1[1]),
        factor * fixX(corner2[0]), factor * fixY(corner2[1]),
        factor * fixX(centerX(corner2[0])), factor * fixY(centerY(corner2[1])),
        factor * fixX(centerX(corner1[0])), factor * fixY(centerY(corner1[1])),
    ), color)


def edge(canvas: ImageDraw.ImageDraw, corner1: tuple[float, float], corner2: tuple[float, float], color: tuple[int, int, int, int]) -> None:
    canvas.polygon((
        factor * corner1[0], factor * corner1[1],
        factor * corner2[0], factor * corner2[1],
        factor * centerX(corner2[0]), factor * centerY(corner2[1]),
        factor * centerX(corner1[0]), factor * centerY(corner1[1]),
    ), color)


def drawEdges(canvas: ImageDraw.ImageDraw, box: tuple[float, float, float, float, Color], color: tuple[int, int, int, int]) -> None:
    if (box[0] > 8):
        edgeShadow(canvas, (box[0], box[1]), (box[0], box[3]), color)
    if (box[1] > 4.5):
        edgeShadow(canvas, (box[0], box[1]), (box[2], box[1]), color)
    if (box[3] < 4.5):
        edgeShadow(canvas, (box[2], box[3]), (box[0], box[3]), color)
    if (box[2] < 8):
        edgeShadow(canvas, (box[2], box[3]), (box[2], box[1]), color)


def drawBoxShadow(im: Image.Image, box: tuple[float, float, float, float, Color], size: tuple[int, int]) -> None:
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    shadowBox = ImageDraw.Draw(shadow)
    shadowBox.rectangle((size[0] / 16 * fixX(box[0]), size[1] / 9 * fixY(box[1]), size[0] / 16 * fixX(box[2]), size[1] / 9 * fixY(box[3])), (0, 0, 0, 220))
    drawEdges(shadowBox, box, (0, 0, 0, 220))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=size[1] / 900 * blur))
    im.alpha_composite(shadow, (0, 0))


def drawBoxBorder(canvas: ImageDraw.ImageDraw, box: tuple[float, float, float, float, Color]) -> None:
    if (box[0] > 8):
        edge(canvas, (box[0], box[1]), (box[0], box[3]), (*Color.interpolate(Colors.black, box[4], colorX(box[0])).color, 255))
    if (box[1] > 4.5):
        edge(canvas, (box[0], box[1]), (box[2], box[1]), (*Color.interpolate(Colors.black, box[4], colorY(box[1])).color, 255))
    if (box[3] < 4.5):
        edge(canvas, (box[2], box[3]), (box[0], box[3]), (*Color.interpolate(Colors.black, box[4], colorY(box[3])).color, 255))
    if (box[2] < 8):
        edge(canvas, (box[2], box[3]), (box[2], box[1]), (*Color.interpolate(Colors.black, box[4], colorX(box[2])).color, 255))


class VideoFormat(Enum):
    mov = 4
    avi = 0


def render_video(name: str, files: list[Background], fps: int = 60, size: tuple[int, int] = (1920, 1080), test: bool = False, videoFormat: VideoFormat = VideoFormat.mov):
    video = cv2.VideoWriter(f'{makeSureFolderExists("Videos", gitignore=True)}/{name}.{videoFormat.name.split(".")[-1]}', videoFormat.value, fps, size)

    for i, image in enumerate(files, start=1):
        print(f"{i} out of {len(files)}")
        if not test:
            combined = image.load(size=size)
        background = Image.new(mode="RGBA", size=size, color=(*image.color.color, 255)) if test else combined
        for img in (root.draw(size=size, test=test) for root in image.children):
            background.paste(img, (0, 0), img)

        pil_image = np.array(background.convert('RGB'))
        open_cv_image = pil_image[:, :, ::-1].copy()
        video.write(open_cv_image)

    cv2.destroyAllWindows()
    video.release()


def render_image(name: str, file: Background, size: tuple[int, int] = (1920, 1080), test: bool = False):
    if not test:
        combined = file.load(size=size)
    background = Image.new(mode="RGBA", size=size, color=(*file.color.color, 255)) if test else combined
    for img in (root.draw(size=size, test=test) for root in file.children):
        background.paste(img, (0, 0), img)
    background.save(f"{makeSureFolderExists('Images', gitignore=True)}/{name}.png")

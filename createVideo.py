from __future__ import annotations
from src.helpers.colors import Colors, Color
from src.helpers.widgets.widgets import *
from src.helpers.curves import Curves

from math import ceil
import cv2
from PIL import Image, ImageDraw
import numpy as np
from functools import cache
from numba import njit
from src.helpers.printer import printer

import math
from typing import TypeVar, Generic, Callable

T = TypeVar('T')
name = "your_file.png"
intencity = 0.9
u_Shininess = 10.0
u_Light_position = np.array([16/9*2.3, -0.5*5, 2*8])
camera = np.array([0.5, 0.5, 2])
blur = 8
factor = 1

def edit_distance(str1: str, str2: str):  
    m, n = len(str1), len(str2)  
    dp = [[0] * (n + 1) for _ in range(m + 1)]  
    for i in range(m + 1):  
        for j in range(n + 1):  
            if i == 0:  
                dp[i][j] = j  
            elif j == 0:  
                dp[i][j] = i  
            elif str1[i - 1] == str2[j - 1]:  
                dp[i][j] = dp[i - 1][j - 1]  
            else:  
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])  
    return dp[m][n]

def string_transformations_iterator(string1: str, string2: str):
    d = edit_distance(string1, string2)
    yield string1
    if d:
      for i, (c1, c2) in enumerate(zip(string1, string2)):
          if string1[i] != string2[i]:
              change_string = string1[:i] + string2[i] + string1[i + 1:]
              d1 = edit_distance(change_string, string2)
              add_string = string1[:i] + string2[i] + string1[i:]
              d2 = edit_distance(add_string, string2)
              delete_string = string1[:i] + string1[i + 1:]
              d3 = edit_distance(delete_string, string2)
              d_min = min(d1, d2, d3)
              if d_min == d1:
                  yield from string_transformations_iterator(change_string, string2)
                  break
              elif d_min == d2:
                  yield from string_transformations_iterator(add_string, string2)
                  break
              else:
                  yield from string_transformations_iterator(delete_string, string2)
                  break
      else:
        if len(string1) < len(string2):
            yield from string_transformations_iterator(string1 + string2[len(string1)], string2)
        else:
            yield from string_transformations_iterator(string1[:len(string2)] + string1[len(string2) + 1:], string2)

@cache
def string_transformations(str1: str, str2: str) -> list[str]:
    return list(string_transformations_iterator(str1, str2))

@njit
def normalize(v):
    return v / np.sqrt(np.sum(v**2))


@cache
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
def _interpolate(pixel_color: tuple[int, int, int], value: float) -> tuple[int, int, int, int]:
    temp = (0.1 + 0.9*value)
    return (int(temp * pixel_color[0]), int(temp * pixel_color[1]), int(temp * pixel_color[2]), 255)
    # return tuple(int((v2 - v1)*x+v1) for v1, v2 in zip(color1, color2))

@njit
def fixScale(v: int, size: tuple[int, int]) -> float:
    return v / (size[1] - 1)

def drawBox(canvas: ImageDraw.ImageDraw, box: tuple[float, float, float, float, Color], size: tuple[int, int]) -> None:
    z = -1.9
    pixel = box[4].color
    for y in range(size[1]):
        _y = fixScale(y, size)
        for x in range(size[0]):
            if not (factor * box[0] < x < factor * box[2] and factor * box[1] < y < factor * box[3]):
                continue
            canvas.point((x, y), _interpolate(pixel, calculate_highlight(fixScale(x, size), _y, z)*intencity))

@cache
def getBox(x_0: float, y_0: float, x_1: float, y_1: float, color: Color, size: tuple[int, int]) -> Image.Image:
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    drawBox(ImageDraw.Draw(img), (x_0, y_0, x_1, y_1, color), size)
    return img

@cache
def getBoxFast(x_0: float, y_0: float, x_1: float, y_1: float, color: Color, size: tuple[int, int], light: tuple[float, float]) -> Image.Image: return Image.fromarray(drawBoxFast(color.color, size, light, x_0, x_1, y_0, y_1))

@njit
def drawBoxFast(color: tuple[int, int, int], size: tuple[int, int], light: tuple[float, float], _x_0: int, _x_1: int, _y_0: int, _y_1: int) -> np.ndarray:
    array = np.zeros((size[1], size[0], 4), dtype=np.uint8)
    scale = 1.85 *math.sqrt(2)*size[0]/2
    phase = 0.1
    darken = 0.05
    x_0 = size[0]*light[0]
    y_0 = size[1]*light[1]
    r = color[0]
    g = color[1]
    b = color[2]
    

    # Image with light spot like a radial gradient
    for y in range(_y_0, min(_y_1, size[1])):
        for x in range(_x_0, min(_x_1, size[0])):
            # Find the distance to the center
            distanceToCenter = math.sqrt((x - x_0) ** 2 + (y - y_0) ** 2)
            # Make it on a scale from 0 to 1
            distanceToCenter = 1-(distanceToCenter / scale + phase)**2 + darken
            # Place the pixel
            array[y, x, 0] = r*distanceToCenter
            array[y, x, 1] = g*distanceToCenter
            array[y, x, 2] = b*distanceToCenter
            array[y, x, 3] = 255
    return array

class Box:
    def __init__(self, x_0: float, y_0: float, x_1: float, y_1: float, fps: int, child: Callable[[int], Widget]) -> None:
        self.x_0: Property[float] = Property(x_0, fps)
        self.y_0: Property[float] = Property(y_0, fps)
        self.x_1: Property[float] = Property(x_1, fps)
        self.y_1: Property[float] = Property(y_1, fps)
        self.color: Property[Color] = Property(Colors.gray.c800, fps, Color.interpolate)
        self.properties: list[Property] = [self.x_0, self.y_0, self.x_1, self.y_1, self.color]
   
        self.child = child
        super().__init__()

    def draw(self, frame: int, screen_size: tuple[int, int], light: tuple[float, float], test: bool = False) -> Image.Image:
        img = Image.new('RGBA', screen_size, (0, 0, 0, 0))
        ratio=(screen_size[1] / 1080)
        size = Size((self.x_1.at_frame(frame)-self.x_0.at_frame(frame))*screen_size[0]/ratio, (self.y_1.at_frame(frame)-self.y_0.at_frame(frame))*screen_size[1]/ratio)
        offset = Offset(self.x_0.at_frame(frame)*screen_size[0]/ratio, self.y_0.at_frame(frame)*screen_size[1]/ratio)
        box = getBoxFast(int(offset.dx*ratio), int(offset.dy*ratio), int((offset.dx+size.width)*ratio), int((offset.dy+size.height)*ratio), self.color.at_frame(frame), screen_size, light)
        img.paste(box, (0, 0), box)
        canvas = ImageDraw.Draw(img)
        # drawBox(canvas, (offset.dx*ratio, offset.dy*ratio, (offset.dx+size.width)*ratio, (offset.dy+size.height)*ratio, Colors.gray.c800), screen_size)
        
        if test:
            canvas.rectangle((offset.dx*ratio, offset.dy*ratio, (offset.dx + size.width)*ratio, (offset.dy + size.height)*ratio), self.color.at_frame(frame).color)
        self.child(frame).draw(canvas,offset, size, ratio)
        return img
    
    @staticmethod
    def normal(child: Callable[[int], Widget]) -> Callable[[int], Box]:
        return lambda fps: Box(0.1, 0.1, 0.9, 0.9, fps, child)
    
    @staticmethod
    def right_tall_outside(child: Callable[[int], Widget]) -> Callable[[int], Box]:
        return lambda fps: Box(1.1, 0.1, 1.35, 0.9, fps, child)


@cache
def background_image(color: Color, size: tuple[int, int], light: tuple[float, float]) -> Image.Image: return Image.fromarray(background_image_fast(color.color, size, light))

@njit
def background_image_fast(color: tuple[int, int, int], size: tuple[int, int], light: tuple[float, float]) -> np.ndarray:
    array = np.zeros((size[1], size[0], 4), dtype=np.uint8)
    scale = 1.85 *math.sqrt(2)*size[0]/2
    phase = 0.1
    darken = 0.05
    x_0 = size[0]*light[0]
    y_0 = size[1]*light[1]
    r = color[0]
    g = color[1]
    b = color[2]
    array[:, :, 3] = 255

    # Image with light spot like a radial gradient
    for y in range(size[1]):
        for x in range(size[0]):
            # Find the distance to the center
            distanceToCenter = math.sqrt((x - x_0) ** 2 + (y - y_0) ** 2)
            # Make it on a scale from 0 to 1
            distanceToCenter = 1-(distanceToCenter / scale + phase)**2 + darken
            # Place the pixel
            array[y, x, 0] = r*distanceToCenter
            array[y, x, 1] = g*distanceToCenter
            array[y, x, 2] = b*distanceToCenter
    return array

class Property(Generic[T]):
    def __init__(self, value: T, fps: int, interpolater = lambda a, b, t: a + (b - a) * t) -> None:
        self.value = value
        self.frame: int = 0
        self.values: dict[int, T] = { 0: value }
        self.interpolater = interpolater
        self.fps = fps

    def wait(self, seconds: float) -> Property[T]:
        self.frame += seconds * self.fps
        return self

    def set(self, value: T) -> Property[T]:
        self.values[ceil(self.frame)] = value
        return self

    def fade(self, value: T, seconds: float, curve: Curves = Curves.easeInOut) -> Property[T]:
        start = ceil(self.frame)
        self.frame += seconds * self.fps
        end = ceil(self.frame)
        start_color = self.at_frame(start)
        for frame in range(start, end + 1):
            self.values[frame] = self.interpolater(start_color, value, curve((frame - start) / (end - start)))
        return self

    def at_frame(self, frame: int) -> T:
        if frame in self.values: return self.values[frame]
        return self.at_frame(frame - 1)
    
class Position:
    def __init__(self, x: float, y: float, fps: int) -> None:
        self.x: Property[float] = Property(x, fps)
        self.y: Property[float] = Property(y, fps)

    def at_frame(self, frame: int) -> tuple[float, float]:
        return (self.x.at_frame(frame), self.y.at_frame(frame))

class Section:
    def __init__(self, video: Video, name: str):
        self.video = video
        self.name = name
        self.color: Property[Color] = Property(Colors.gray.c800, video.fps, Color.interpolate)
        self.light: Position = Position(0.65, 0.0, video.fps)
        self.properties: list[Property] = [self.color, self.light.x, self.light.y]
        self.drawables: list[Box] = []

    def add(self, drawable: Callable[[int], Box]) -> Box:
        temp = drawable(self.video.fps)
        self.drawables.append(temp)
        self.properties.extend(temp.properties)
        return temp
    
    def addProperty(self, value: T, interpolater = lambda a, b, t: a + (b - a) * t) -> Property[T]:
        temp = Property(value, self.video.fps, interpolater)
        self.properties.append(temp)
        return temp
        
class Video:
    def __init__(self, filename: str, size: tuple[int, int], fps: int, test: bool = False):
        self.filename = filename
        self.size = size
        self.fps = fps
        self.test = test
        self.sections: list[Section] = []

    def section(self, name: str) -> Section:
        chapter = Section(self, name)
        self.sections.append(chapter)
        return chapter
    
    def render(self) -> None:
        video = cv2.VideoWriter(self.filename, 4, self.fps, self.size)
        
        for section in self.sections:
            frames = ceil(max(property.frame for property in section.properties))
            for frame in range(frames + 1):
              print(f"Rendering frame {frame}/{frames}", end="\r")
              image = background_image(section.color.at_frame(frame), self.size, section.light.at_frame(frame)).copy()
              with printer(None):
                for img in (drawable.draw(frame, screen_size=self.size, light=section.light.at_frame(frame), test=self.test) for drawable in section.drawables):
                  image.paste(img, (0, 0), img)
              pil_image = np.array(image.convert('RGB'))
              open_cv_image = pil_image[:, :, ::-1].copy()
              video.write(open_cv_image)

        cv2.destroyAllWindows()
        video.release()

class Layouts:
    normal_with_tall_on_right = [(0.1, 0.1, 0.9, 0.9), (1.1, 0.1, 1.35, 0.9)]
    share_with_tall_on_right = [(0.05, 0.1, 0.65, 0.9), (0.7, 0.1, 0.95, 0.9)]

class WindowManager:
    def __init__(self, *windows: Box) -> None:
        self.windows = windows

    def wait(self, seconds: float) -> WindowManager:
        for window in self.windows:
            window.x_0.wait(seconds)
            window.y_0.wait(seconds)
            window.x_1.wait(seconds)
            window.y_1.wait(seconds)
        return self
    
    def fade(self, layout: list[tuple[int, int, int, int]], seconds: float, curve: Curves = Curves.easeInOut) -> WindowManager:
        for window, (x_0, y_0, x_1, y_1) in zip(self.windows, layout):
            window.x_0.fade(x_0, seconds, curve)
            window.y_0.fade(y_0, seconds, curve)
            window.x_1.fade(x_1, seconds, curve)
            window.y_1.fade(y_1, seconds, curve)
        return self
    
    def set(self, layout: list[tuple[int, int, int, int]]) -> WindowManager:
        for window, (x_0, y_0, x_1, y_1) in zip(self.windows, layout):
            window.x_0.set(x_0)
            window.y_0.set(y_0)
            window.x_1.set(x_1)
            window.y_1.set(y_1)
        return self




video = Video("Videos/test.mov", size=(3840//4, 2160//4), fps=60//2, test=False)


# Driver Code
s1 = "Change into sthot"
s2 = "Change this into that"



def stringIntepolater(start: str, end: str, x: float) -> str:
  transformations = string_transformations(start, end)
  i = int((len(transformations) - 1) * x)
  return transformations[i]

intro = video.section("Intro")
intro.color.set(Colors.blue).wait(0.5) #.fade(Colors.green, 1).wait(0.5).fade(Colors.red, 1).wait(0.5)
text = intro.addProperty("""class Code:
    @staticmethod
    def normal(child: Callable[[int], Widget]) -> Callable[[int], Box]:
        return lambda fps: Box(0.1, 0.1, 0.9, 0.9, fps, child)
    
    @staticmethod
    def right_tall_outside(child: Callable[[int], Widget]) -> Callable[[int], Box]:
        return lambda fps: Box(1.1, 0.1, 1.35, 0.9, fps, child)
""", stringIntepolater).wait(1).fade("""class Magnus:
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def greet(self) -> None:
        print(f"Hello, my name is {self.name}!")
""", 5)

editor = intro.add(
  Box.normal(
    lambda frame: FileEditor(
      filename="example.py",
      child=Code(
        text.at_frame(frame),
        fontSize=24,
        # fontSize=float("inf"),
        # functions={"dtu", "set", "get"},
        # classes={"Parameters", "Database", "Colors"},
        # notModules={"database"}
      ),
    )
  )
)
editor.color.wait(1).fade(Colors.gray.c900, 1).wait(1).fade(Colors.gray.c800, 1).wait(1)
terminal = intro.add(
  Box.right_tall_outside(
    lambda frame: FileEditor(
      filename="Terminal",
      child=Console(
"""C:\\Python>python example.py
Hello World!

C:\\Python>""",
        fontSize=24,
      ),
    ),
  )
)
terminal.color.set(Colors.gray.c900)

windowManager = WindowManager(editor, terminal).wait(1).fade(Layouts.share_with_tall_on_right, 1).wait(1).fade(Layouts.normal_with_tall_on_right, 1,  Curves.linear).wait(1)

video.render()


from IPython.display import Image
Image("../images/fun-fish.png")

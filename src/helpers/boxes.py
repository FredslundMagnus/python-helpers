from src.helpers.colors import Color, Colors
from typing import TypeAlias

Box: TypeAlias = tuple[float, float, float, float, Color]

class Boxes:
    def normal(color: Color = Colors.gray.c800) -> Box:
        return (16/9, 1, 16-16/9, 8, color)
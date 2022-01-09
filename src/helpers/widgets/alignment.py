from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Alignment:
    x: float = 0.0
    y: float = 0.0

    def __call__(self) -> Alignment:
        return self

    @staticmethod
    def topLeft() -> Alignment:
        return Alignment(-1.0, -1.0)

    @staticmethod
    def topCenter() -> Alignment:
        return Alignment(0.0, -1.0)

    @staticmethod
    def topRight() -> Alignment:
        return Alignment(1.0, -1.0)

    @staticmethod
    def centerLeft() -> Alignment:
        return Alignment(-1.0, 0.0)

    @staticmethod
    def center() -> Alignment:
        return Alignment(0.0, 0.0)

    @staticmethod
    def centerRight() -> Alignment:
        return Alignment(1.0, 0.0)

    @staticmethod
    def bottomLeft() -> Alignment:
        return Alignment(-1.0, 1.0)

    @staticmethod
    def bottomCenter() -> Alignment:
        return Alignment(0.0, 1.0)

    @staticmethod
    def bottomRight() -> Alignment:
        return Alignment(1.0, 1.0)

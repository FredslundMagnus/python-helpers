from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Alignment:
    x: float = 0.0
    y: float = 0.0

    @property
    @classmethod
    def topLeft(cls) -> Alignment:
        return Alignment(-1.0, -1.0)

    @property
    @classmethod
    def topCenter(cls) -> Alignment:
        return Alignment(0.0, -1.0)

    @property
    @classmethod
    def topRight(cls) -> Alignment:
        return Alignment(1.0, -1.0)

    @property
    @classmethod
    def centerLeft(cls) -> Alignment:
        return Alignment(-1.0, 0.0)

    @property
    @classmethod
    def center(cls) -> Alignment:
        return Alignment(0.0, 0.0)

    @property
    @classmethod
    def centerRight(cls) -> Alignment:
        return Alignment(1.0, 0.0)

    @property
    @classmethod
    def bottomLeft(cls) -> Alignment:
        return Alignment(-1.0, 1.0)

    @property
    @classmethod
    def bottomCenter(cls) -> Alignment:
        return Alignment(0.0, 1.0)

    @property
    @classmethod
    def bottomRight(cls) -> Alignment:
        return Alignment(1.0, 1.0)

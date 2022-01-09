from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Alignment:
    x: float = 0.0
    y: float = 0.0

    @property
    def topLeft(self) -> Alignment:
        return Alignment(-1.0, -1.0)

    @property
    def topCenter(self) -> Alignment:
        return Alignment(0.0, -1.0)

    @property
    def topRight(self) -> Alignment:
        return Alignment(1.0, -1.0)

    @property
    def centerLeft(self) -> Alignment:
        return Alignment(-1.0, 0.0)

    @property
    def center(self) -> Alignment:
        return Alignment(0.0, 0.0)

    @property
    def centerRight(self) -> Alignment:
        return Alignment(1.0, 0.0)

    @property
    def bottomLeft(self) -> Alignment:
        return Alignment(-1.0, 1.0)

    @property
    def bottomCenter(self) -> Alignment:
        return Alignment(0.0, 1.0)

    @property
    def bottomRight(self) -> Alignment:
        return Alignment(1.0, 1.0)

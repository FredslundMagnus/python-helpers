from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Edges:
    top: float = 0.0
    right: float = 0.0
    bottom: float = 0.0
    left: float = 0.0

    @staticmethod
    def symmetric(vertical: float = 0.0, horizontal: float = 0.0) -> Edges:
        return Edges(top=vertical, bottom=vertical, right=horizontal, left=horizontal)

    @staticmethod
    def all(value: float = 0.0) -> Edges:
        return Edges(top=value, bottom=value, right=value, left=value)

    @staticmethod
    def only(top: float = 0.0, bottom: float = 0.0, right: float = 0.0, left: float = 0.0) -> Edges:
        return Edges(top=top, bottom=bottom, right=right, left=left)

    @property
    @classmethod
    def zero(cls) -> Edges:
        return Edges()

from enum import Enum


class Curve:
    def __call__(self, x: float) -> float:
        return x


class Linear(Curve):
    def __call__(self, x: float) -> float:
        return x


class Curves:
    linear = Linear()

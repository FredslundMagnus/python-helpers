from enum import Enum


class Curve:
    def __call__(self, x: float) -> float:
        return x


class Linear(Curve):
    def __call__(self, x: float) -> float:
        return x


class EaseInOut(Curve):
    def __call__(self, x: float) -> float:
        if x < 0.5:
            return 2 * x * x
        return (-2 * x * x) + (4 * x) - 1


class EaseIn(Curve):
    def __call__(self, x: float) -> float:
        return x * x


class EaseOut(Curve):
    def __call__(self, x: float) -> float:
        return -(x * (x - 2))


class Curves:
    linear = Linear()
    easeOut = EaseOut()
    easeIn = EaseIn()
    easeInOut = EaseInOut()

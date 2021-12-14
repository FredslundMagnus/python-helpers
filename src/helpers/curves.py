from enum import Enum


def linear(x: float) -> float:
    return x


class Curves(Enum):
    linear = linear

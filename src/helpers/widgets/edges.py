from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


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

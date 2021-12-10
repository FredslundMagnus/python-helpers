from dataclasses import dataclass
from dtu.server import parameters, Parameters


class Defaults(metaclass=Parameters):
    b: float = 2.0
    a: int = 1
    d: str = "fd"


print(Defaults().a)
print(Defaults.a)

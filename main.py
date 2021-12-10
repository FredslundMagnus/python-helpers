
from dtu.server import Parameters, dataclass

@dataclass
class Defaults(Parameters):
    name: str = "local"
    n: int = 1
    GPU: bool = False
    time: int = 3600

    b: float = 2.0
    a: int = 1
    d: str = "fd"

    def run(cls, b: float, d: str, a: int) -> None:
        print(b,d, a)


Defaults.start()


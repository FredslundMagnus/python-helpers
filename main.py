from __future__ import annotations
from src.helpers.server import Parameters, dtu
from src.helpers.database import Database
from src.helpers.printer import print, Colors

@dtu
class Defaults(Parameters):
    name: str = "local"
    instances: int = 1
    GPU: bool = False
    time: int = 3600
    # database: Database = Database("dtu-server-test")

    b: float = 2.0
    a: int = 1
    d: str = "fd"

    def run(self, b: float, d: str) -> None:
        # database.set("doc1", {"a": a, "b": b})
        # print(database.get("doc1"))
        print(b,d, self.time, color=Colors.red)


Defaults.start()

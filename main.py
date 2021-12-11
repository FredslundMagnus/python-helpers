from __future__ import annotations
from src.helpers.server import Parameters, dtu
from src.helpers.database import Database

@dtu
class Defaults(Parameters):
    name: str = "local"
    instances: int = 1
    GPU: bool = False
    time: int = 3600
    database: Database = Database("dtu-server-test")

    b: float = 2.0
    a: int = 1
    d: str = "fd"

    def run(self, b: float, d: str, a: int, database: Database) -> None:
        database.set("doc1", {"a": a, "b": b})
        print(database.get("doc1"))
        print(b,d, self.time)


Defaults.start()


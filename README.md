# Welcome
```bash
pip install git+https://github.com/FredslundMagnus/dtu-server.git
```
or 
```bash
C:/path/to/python.exe -m pip install --upgrade --force-reinstall git+https://github.com/FredslundMagnus/dtu-server.git
```

# Server
Example of main.py
```python
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
```

example of generate.py
```python
from main import Defaults

Defaults("Test1", b=4, d="dsf")
```
It will check types

# Database
## Create a Firebase Project
Give the project a name
Enable firebase analytics
Choose default firebase project
## Generate Private Key
Go to Project Settings -> Service Accounts -> Generate new private key
## Save the Key
Create a new folder somewhere on your computer
fx: C:\Users\magnu\Documents\private_keys
Then place the json-file you just downloaded in this folder.
fx: C:\Users\magnu\Documents\private_keys\project_id-firebase.json
Then add the folder to your path "System"-environment variables (Cannot be user). 
Close VS Code and any running python instances
Optionally restart computer

# Create Firestore Database
Click Create database
Start in production mode
Choose eur3 (europe-west)
Click Enable


## Import Database
```python
from helpers.database import Database

database = Database("project_id", collection="collection_name") # Collection is required and will be default.
```
or
```python
from helpers.server import Parameters, dtu
from helpers.database import Database

@dtu
class Defaults(Parameters):
    name: str = "local"
    ...
    database: Database = Database("project_id") # Collection will automatically be name ("local" or overwritten by server).
    ...

    def run(self, database: Database):
        # Use normally
        databse.set(...)
        database.get(...)
```


## Use Database
```python
database.set("doc1", {"name": "value", "booleans": False, "strings": "sf", "floats": 4.3, "integers": 4})
print(database.get("doc1"))

for v in database.getAll():
    print(v)
```
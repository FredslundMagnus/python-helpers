from os import mkdir
from os.path import exists


def makeSureFolderExists(name: str, gitignore: bool = False) -> str:
    if not exists(name):
        mkdir(name)
    if not gitignore:
        return name
    if not exists(".gitignore"):
        with open(".gitignore", "w+") as f:
            f.write(name+'/*')
    return name

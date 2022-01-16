from os import mkdir
from os.path import exists


def makeSureFolderExists(name: str, gitignore: bool = False) -> str:
    if not exists(name):
        mkdir(name)
    if not gitignore:
        return name
    with open(".gitignore", "a+") as f:
        for line in f:
            print(line, line == name+'/*', name+'/*')
            # if line == name+'/*':
            #     print()
        # f.write(name+'/*')
    return name

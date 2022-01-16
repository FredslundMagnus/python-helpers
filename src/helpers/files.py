from os import mkdir
from os.path import exists


class GitIgnore:
    file: str = ".gitignore"

    @property
    @staticmethod
    def exists() -> bool:
        return exists(GitIgnore.file)

    @staticmethod
    def generate() -> None:
        GitIgnore.add("*pyc")
        GitIgnore.add("__pycache__\n")

    @staticmethod
    def add(line) -> None:
        print(GitIgnore.exists)
        if not GitIgnore.exists:
            with open(GitIgnore.file, "w+") as f:
                f.write(f"{line}\n")


def makeSureFolderExists(name: str, gitignore: bool = False) -> str:
    if not exists(name):
        mkdir(name)
    print(gitignore)
    if gitignore:
        GitIgnore.add(name + '/*')
    return name

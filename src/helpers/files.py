from os import mkdir
from os.path import exists


class GitIgnore:
    file: str = ".gitignore"

    @staticmethod
    def exists() -> bool:
        return exists(GitIgnore.file)

    @staticmethod
    def generate() -> None:
        if not GitIgnore.exists():
            with open(GitIgnore.file, "w"):
                pass
        GitIgnore.add("*pyc")
        GitIgnore.add("__pycache__")
        GitIgnore.add(".vscode/*")

    @staticmethod
    def add(line: str) -> None:
        GitIgnore.generate()

        with open(GitIgnore.file, "a") as f:
            f.write(f"\n{line}")

        GitIgnore.fix()

    @staticmethod
    def fix() -> None:
        if not GitIgnore.exists():
            return
        with open(GitIgnore.file, "r") as f:
            file = f.read().splitlines()
        with open(GitIgnore.file, "w") as f:
            for line in (l.strip() for l in sorted(set(file)) if l.strip()):
                f.write(f"{line}\n")


def makeSureFolderExists(name: str, gitignore: bool = False) -> str:
    if not exists(name):
        mkdir(name)
    if gitignore:
        GitIgnore.add(name + '/*')
    return name

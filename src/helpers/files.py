from os import mkdir
from os.path import exists


class GitIgnore:
    file: str = ".gitignore"

    @staticmethod
    def exists() -> bool:
        return exists(GitIgnore.file)

    @staticmethod
    def generate() -> None:
        GitIgnore.add("*pyc")
        GitIgnore.add("__pycache__")
        GitIgnore.add(".vscode/*")

    @staticmethod
    def add(line: str) -> None:
        line = line.strip()
        if not GitIgnore.exists():
            with open(GitIgnore.file, "w") as f:
                f.write(f"{line}")
        else:
            with open(GitIgnore.file, "r") as f:
                for _line in f:
                    if _line.strip() == line:
                        return
                print(f.read())
                print(f.read())
                shouldAddNewline = True if len(f.read()) == 0 else f.read()[-1] != '\n'
            with open(GitIgnore.file, "a") as f:
                print(1, _line)
                print(2, _line == '')
                print(3, shouldAddNewline)
                newline = '\n' if shouldAddNewline else ''
                f.write(f"{newline}{line}")


def makeSureFolderExists(name: str, gitignore: bool = False) -> str:
    if not exists(name):
        mkdir(name)
    print(gitignore)
    if gitignore:
        GitIgnore.add(name + '/*')
    return name

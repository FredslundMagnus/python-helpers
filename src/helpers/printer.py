from __future__ import annotations
import builtins
from helpers.colors import Color, Colors
from contextlib import redirect_stdout as printer
from sys import stdout as terminal

terminal, printer, Colors

def colored(object: object, color: Color):
    return f'\x1B[38;2;{color.color[0]};{color.color[1]};{color.color[2]}m{object}\x1B[0m'

def print(*values: object, sep: str | None = ' ', end: str | None = '\n', color: Color | None = None) -> None:
    if color is None:
        builtins.print(*values, sep=sep, end=end)
    else:
        text = sep.join(str(v) for v in values)
        builtins.print(colored(text, color), end=end)


from __future__ import annotations

from helpers.colors import Color

import pygments as pm
import pygments.lexers as lexers
from pygments.token import Token


class Language:
    extention: str
    color_booleans: Color = Color(86, 156, 214)
    color_systemWords: Color = Color(197, 134, 192)
    color_classes: Color = Color(78, 201, 176)
    color_symbols: Color = Color(255, 255, 255)
    color_functions: Color = Color(220, 220, 170)
    color_numerics: Color = Color(181, 206, 168)
    color_default: Color = Color(156, 220, 254)
    color_comments: Color = Color(0, 255, 0)
    color_strings: Color = Color(255, 0, 0)

    def colorize(self, code: str) -> list[list[Color]]:
        pass


class Python(Language):
    extention: str = "py"

    def colorize(self, code: str) -> list[list[Color]]:
        lexer = lexers.get_lexer_by_name('python')
        output: list[list[Color]] = []
        line = []
        for token, chars in pm.lex(code, lexer):
            if chars == "\n":
                output.append(line)
                line = []
                continue
            for char in chars:
                print(chars, token, token == Token.String, token == Token.Literal.String, token == Token.Literal.String.Double, token == Token.Text)
                if token == Token.String:
                    line.append(Python.color_strings)
                else:
                    line.append(Python.color_functions)
        output.append(line)
        return output
        # return [[Python.color_systemWords for char in line] for line in code.splitlines()]


class Dart(Language):
    extention: str = "dart"

    def colorize(self, code: str) -> list[list[Color]]:
        pass


class Rust(Language):
    extention: str = "rs"

    def colorize(self, code: str) -> list[list[Color]]:
        pass


class Languages:
    languages: list[Language] = [Python(), Dart(), Rust()]
    python: Language = Python()
    dart: Language = Dart()
    rust: Language = Rust()

    @staticmethod
    def fromExtension(extension: str) -> Language:
        return [lang for lang in Languages.languages if lang.extention == extension][0]

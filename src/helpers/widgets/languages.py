from __future__ import annotations

from helpers.colors import Color

from pygments import lex
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_by_name
from pygments.token import Token as Tokens, _TokenType as Token


class Language:
    extention: str
    lexer: Lexer
    strings: set = Tokens.Literal.String.subtypes
    color_booleans: Color = Color(86, 156, 214)
    color_systemWords: Color = Color(197, 134, 192)
    color_classes: Color = Color(78, 201, 176)
    color_symbols: Color = Color(255, 255, 255)
    color_functions: Color = Color(220, 220, 170)
    color_numerics: Color = Color(181, 206, 168)
    color_default: Color = Color(156, 220, 254)
    color_comments: Color = Color(106, 153, 85)
    color_strings: Color = Color(206, 145, 120)

    def tokenize(self, code: str) -> list[list[Token]]:
        output: list[list[Color]] = []
        line = []
        for token, chars in lex(code, self.lexer):
            if chars == "\n":
                output.append(line)
                line = []
                continue
            for _ in chars:
                line.append(token)
        output.append(line)
        return output

    def colorize(self, code: str) -> list[list[Color]]:
        tokens: list[list[Token]] = self.tokenize(code)
        print(tokens)
        return [[self.color(token) for token in line] for line in tokens]

    def color(self, token: Token) -> Color:
        if token in self.strings:
            return self.color_strings
        if token in self.strings:
            return self.color_strings
        return self.color_functions


class Python(Language):
    extention: str = "py"
    lexer: Lexer = get_lexer_by_name('python')


class Dart(Language):
    extention: str = "dart"
    lexer: Lexer = get_lexer_by_name('dart')


class Rust(Language):
    extention: str = "rs"
    lexer: Lexer = get_lexer_by_name('rust')


class Languages:
    languages: list[Language] = [Python(), Dart(), Rust()]
    python: Language = Python()
    dart: Language = Dart()
    rust: Language = Rust()

    @staticmethod
    def fromExtension(extension: str) -> Language:
        return [lang for lang in Languages.languages if lang.extention == extension][0]

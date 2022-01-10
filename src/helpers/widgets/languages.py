from __future__ import annotations

from helpers.colors import Color, Colors

from pygments import lex
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_by_name
from pygments.token import Token as Tokens, _TokenType as Token

print(Tokens.Literal.String.subtypes)


class Language:
    extention: str
    lexer: Lexer
    strings: set = Tokens.Literal.String.subtypes
    comments: set = Tokens.Comment.subtypes
    numbers: set = Tokens.Literal.Number.subtypes
    symbols: set = {Tokens.Punctuation, Tokens.Operator}
    color_booleans: Color = Color(86, 156, 214)
    color_systemWords: Color = Color(197, 134, 192)
    color_classes: Color = Color(78, 201, 176)
    color_symbols: Color = Color(255, 255, 255)
    color_functions: Color = Color(220, 220, 170)
    color_numbers: Color = Color(181, 206, 168)
    color_default: Color = Color(156, 220, 254)
    color_comments: Color = Color(106, 153, 85)
    color_strings: Color = Color(206, 145, 120)
    # SYMBOLS = {' ', ':', ',' , '=', '(', ')', '-', '>', '<', '*', '+', '.'}
    FUNCTIONS = {'print'}
    CLASSES = {'int', 'bool'}
    BOOLEANS = {'True', 'False', 'not', 'and', 'or', 'in', 'None', 'is', 'lambda', 'class', 'def'}
    SYSTEMWORDS = {'while', 'if', 'return', 'for', 'else', 'raise', 'pass', 'break', 'try', 'except', 'yield', 'continue', 'assert'}

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
        print(set.union(*[set(token) for token in tokens]))
        return [[self.color(token) for token in line] for line in tokens]

    def color(self, token: Token) -> Color:
        if token in self.strings:                     #
            return self.color_strings                 #
        if token in self.comments:                    #
            return self.color_comments                #
        if token in self.numbers:                     #
            return self.color_numbers                 #
        if token in self.symbols:                     #
            return self.color_symbols                 #
        if token == Tokens.Name:
            return self.color_default
        if token == Tokens.Keyword.Constant:          #
            return self.color_booleans                #
        if token == Tokens.Keyword:
            return self.color_systemWords
        if token == Tokens.Keyword.Namespace:
            return self.color_functions
        if token == Tokens.Name.Namespace:
            return self.color_classes
        if token == Tokens.Name.Builtin:
            return Colors.red
        if token == Tokens.Literal.String.Interpol:
            return Colors.orange
        if token == Tokens.Text:
            return Colors.pink

        print(token)


class Python(Language):
    extention: str = "py"
    lexer: Lexer = get_lexer_by_name('python')

    def tokenize(self, code: str) -> list[list[Token]]:
        output: list[list[Color]] = []
        line = []
        for token, word in lex(code, self.lexer):
            if word == "\n":
                output.append(line)
                line = []
                continue
            for _ in word:
                if token in self.comments:
                    line.append(token)
                elif token in self.strings:
                    line.append(token)
                elif word in {'import'}:
                    line.append(Tokens.Keyword)
                else:
                    line.append(token)
        output.append(line)
        return output


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

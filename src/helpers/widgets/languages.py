from __future__ import annotations

from helpers.colors import Color, Colors

from pygments import lex
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_by_name
from pygments.token import Token as Tokens, _TokenType as Token


class Language:
    extention: str
    lexer: Lexer
    strings: set = {Tokens.Literal.String.Symbol, Tokens.Literal.String.Escape, Tokens.Literal.String.Double, Tokens.Literal.String.Backtick, Tokens.Literal.String.Char,
                    Tokens.Literal.String.Doc, Tokens.Literal.String.Single, Tokens.Literal.String.Heredoc, Tokens.Literal.String.Other, Tokens.Literal.String.Delimiter, Tokens.Literal.String.Regex}
    comments: set = Tokens.Comment.subtypes
    numbers: set = Tokens.Literal.Number.subtypes
    symbols: set = {Tokens.Punctuation, Tokens.Operator, Tokens.Text}
    systemwords: set = {Tokens.Keyword, Tokens.Keyword.Namespace}
    logicals: set = {Tokens.Keyword.Constant, Tokens.Literal.String.Interpol, Tokens.Operator.Word, Tokens.Literal.String.Affix}
    builtin_classes: set = {"bool", "bytearray", "bytes", "classmethod", "complex", "dict", "property", "range", "reversed",
                            "enumerate", "filter", "float", "frozenset", "int", "memoryview", "map", "list", "object", "set",
                            "slice", "staticmethod", "str", "super", "tuple", "type", "zip"}
    builtin_functions: set = {"aiter", "anext", "ascii", "breakpoint", "callable", "exec", "help",
                              "eval", "format", "getattr", "globals", "hasattr", "hash", "hex", "id", "input", "isinstance", "__import__",
                              "abs", "all", "any", "bin", "chr", "compile", "delattr", "dir", "divmod", "issubclass", "iter", "vars", "sorted",
                              "len", "locals", "max", "min", "next", "oct", "open", "ord", "pow", "print", "repr", "round", "setattr", "sum"}
    color_logicals: Color = Color(86, 156, 214)
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
        pass

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
        if token in self.systemwords:                 #
            return self.color_systemWords             #
        if token in self.logicals:                    #
            return self.color_logicals                #
        if token == Tokens.Name.Namespace:            # Modules
            return self.color_symbols                 # Modules
        if token == Tokens.Name:                      # Variables
            return self.color_default                 # Variables
        if token == Tokens.Name.Class:                # Classes
            return self.color_classes                 # Classes
        if token == Tokens.Name.Function:             # Functions
            return self.color_functions               # Functions
        print(token)
        return Colors.red


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
                elif word in {'import', 'in'}:
                    line.append(Tokens.Keyword)
                elif token == Tokens.Name.Builtin or word in self.builtin_functions:  # Figure aot builtin methods
                    if word in self.builtin_classes:
                        line.append(Tokens.Name.Class)
                    elif word in self.builtin_functions:
                        line.append(Tokens.Name.Function)
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

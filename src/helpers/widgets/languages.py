from __future__ import annotations


class Language:
    extention: str = ""


class Python(Language):
    extention: str = "py"


class Dart(Language):
    extention: str = "dart"


class Rust(Language):
    extention: str = "rs"


class Languages:
    languages: list[Language] = [Python(), Dart(), Rust()]
    python: Language = Python()
    dart: Language = Dart()
    rust: Language = Rust()

    @staticmethod
    def fromExtension(extension: str) -> Language:
        return [lang for lang in Languages.languages if lang.extention == extension][0]

from os.path import join


class Font:
    def __init__(self, file: str) -> None:
        self.file = file


class Fonts:
    CascadiaCode: Font = Font(join("Fonts", "Cascadia", "CascadiaCode.ttf"))

from src.helpers.colors import Colors
from src.helpers.image.background import Background

Background(color=Colors.brown, boxes=[(0, 0, 16, 9)]).load(size=(1920, 1080))

Background(color=Colors.brown, boxes=[(16/9, 1, 16-16/9, 8)]).load(size=(1920, 1080))

Background(color=Colors.brown, boxes=[(1, 1, 7.5, 8, Colors.green), (8.5, 1, 15, 8, Colors.red)]).load(size=(1920, 1080))

Background(color=Colors.brown, boxes=[(1, 1, 7.5, 8, Colors.blue), (8.5, 1, 15, 8)]).load(size=(1920, 1080))

Background(color=Colors.brown, boxes=[(1, 1, 5, 8, Colors.blue), (6, 1, 10, 8), (11, 1, 15, 8, Colors.green)]).load(size=(1920, 1080))

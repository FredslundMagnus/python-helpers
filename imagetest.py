from helpers.colors import Colors
from helpers.image.background import Background

Background(color=Colors.brown, boxes=[(0, 0, 16, 9)]).render(size=(1920//2, 1080//2))

import arcade
from EnvironmentVariables import *

class Wall(arcade.Sprite):
    def __init__(self, cords):
        x, y = cords
        super().__init__(WALL_TEXTURE, 1, x,y)

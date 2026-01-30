import arcade
from EnvironmentVariables import *

class Apple(arcade.Sprite):
    def __init__(self, cords):
        x,y = cords
        super().__init__(APPLE_TEXTURE, 0.05, x, y)

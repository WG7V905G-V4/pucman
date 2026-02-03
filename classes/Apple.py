import arcade
from LevelTools import *

class Apple(arcade.Sprite):
    def __init__(self, cords):
        x,y = cords
        super().__init__(ENV_VAR_DICT["APPLE_TEXTURE"], ENV_VAR_DICT["APPLE_SCALE"], x,y)
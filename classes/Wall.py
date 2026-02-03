import arcade
from LevelTools import *

class Wall(arcade.Sprite):
    def __init__(self, cords):
        x,y = cords

        super().__init__(ENV_VAR_DICT['WALL_TEXTURE'], ENV_VAR_DICT['WALL_SCALE'], x,y)

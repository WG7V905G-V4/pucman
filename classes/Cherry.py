import arcade
from LevelTools import *

class Cherry(arcade.Sprite):
    def __init__(self, cords):
        x,y = cords
        
        super().__init__(ENV_VAR_DICT["CHERRY_TEXTURE"], ENV_VAR_DICT["CHERRY_SCALE"], x,y)
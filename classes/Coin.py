import arcade
from LevelTools import *

class Coin(arcade.Sprite):
    def __init__(self, cords):
        x,y = cords
        super().__init__(ENV_VAR_DICT["COIN_TEXTURE"], ENV_VAR_DICT["COIN_SCALE"], x,y)
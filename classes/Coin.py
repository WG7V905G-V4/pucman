import arcade
from EnvironmentVariables import *

class Coin(arcade.Sprite):
    def __init__(self, cords):
        x,y = cords
        super().__init__(COIN_TEXTURE, 1, x ,y)
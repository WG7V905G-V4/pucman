import arcade
from EnvironmentVariables import *

class Coin(arcade.Sprite):
    def __init__(self, cords):
        x,y = cords
        super().__init__(
            texture=arcade.make_circle_texture(diameter=COIN_DIAMETER,
                                               color=COIN_COLOR),
            center_x=x,
            center_y=y,
        )
import arcade
from EnvironmentVariables import *

class Wall(arcade.Sprite):
    def __init__(self, cords):
        x, y = cords
        texture = arcade.make_soft_square_texture(
            TILE_SIZE,
            WALL_COLOR,
            225,
            0
        )
        super().__init__(
            texture,
            center_x=x,
            center_y=y
        )

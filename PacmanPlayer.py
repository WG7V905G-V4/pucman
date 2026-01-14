import arcade
from main import TILE_SIZE
from Character import Character


class Pacman(Character):
    def __init__(self, x, y, color):
        super().__init__()
        radius = TILE_SIZE//2 - 2
        texture = arcade.make_circle_texture(radius * 2, color)
        self.texture = texture
        self.center_y = y
        self.center_x = x


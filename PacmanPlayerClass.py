import arcade
from main import TILE_SIZE
from Character import Character


class Pacman(Character):
    def __init__(self, x, y, color):
        super().__init__()
        texture = arcade.make_circle_texture(radius * 2, color)
        self.texture = texture






import arcade
from main import TILE_SIZE
class Character(arcade.Sprite):
    def __init__(self, center_x, center_y, speed):
        super().__init__()
        self.radius = TILE_SIZE // 2 - 2
        self.width = 30
        self.height = 30
        self.center_x = center_x
        self.center_y = center_y
        self.speed = speed
        self.change_x = 0
        self.change_y = 0
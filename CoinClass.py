from main import TILE_SIZE
import arcade
class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 10
        self.center_x = x
        self.center_y = y
        texture = arcade.make_circle_texture(TILE_SIZE, arcade.color.YELLOW)
        self.texture = texture




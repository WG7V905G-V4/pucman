from main import TILE_SIZE
import arcade
class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 10
        self.center_x = x
        self.center_y = y
        self.size = TILE_SIZE//2
        texture = arcade.make_circle_texture(self.size*2, arcade.color.YELLOW)
        self.texture = texture




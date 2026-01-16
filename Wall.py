import arcade

TILE_SIZE = 32


class BlueWall(arcade.Sprite):
    def __init__(self, x,y):
        super().__init__()

        self.size = TILE_SIZE

        self.texture = arcade.make_soft_square_texture(32, arcade.color.BLUE, 225, 0)

        self.center_x, self.center_y = x,y

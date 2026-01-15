import arcade

TILE_SIZE = 32


class BlueWall(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        size = TILE_SIZE - 2

        self.texture = arcade.make_create_rect_texture(size, size, arcade.color.BLUE)

        self.center_x = x
        self.center_y = y
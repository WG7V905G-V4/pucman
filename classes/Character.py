import arcade

from EnvironmentVariables import TILE_SIZE

KEY_CONFIG = {
    #rotation_angle, change_x, change_y, matrix_check_row, matrix_check_col
    arcade.key.UP: [(-1, 0, 1), (-1, 0)],
    arcade.key.DOWN: [(1, 0, -1),(1, 0)],
    arcade.key.LEFT: [(2, -1, 0),(0, -1)],
    arcade.key.RIGHT:[(0, 1, 0),(0, 1)]
}


class Character(arcade.Sprite):
    def __init__(self, texture, cords, speed, rotation_angle):
        super().__init__(texture, 1)
        self.center_x, self.center_y = cords
        self.speed = speed
        self.rotation_angle = rotation_angle
        self.m_x , self.m_y = self.center_x//TILE_SIZE, self.center_y//TILE_SIZE
        self.key= None

    def update(self, *args, **kwargs):
        self.m_x , self.m_y = self.center_x//TILE_SIZE, self.center_y//TILE_SIZE
        super().update()

    def move(self, key):
        if key in KEY_CONFIG:
            self.angle, self.change_x, self.change_y =tuple(
                x * y for x, y in zip(
                    (self.rotation_angle, self.speed, self.speed),
                    KEY_CONFIG[key][0]
                )
            )

    def stop(self):
        if self.center_x % (TILE_SIZE//2) == 0 and self.center_y %(TILE_SIZE//2) == 0:
           super().stop()
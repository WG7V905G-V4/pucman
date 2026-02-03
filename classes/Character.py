import arcade
from LevelTools import *

KEY_CONFIG = {
    #rotation_angle, change_x, change_y, matrix_check_row, matrix_check_col
    arcade.key.UP: (-1, 0, 1),
    arcade.key.DOWN: (1, 0, -1),
    arcade.key.LEFT: (2, -1, 0),
    arcade.key.RIGHT: (0, 1, 0),
}


class Character(arcade.Sprite):
    def __init__(self, texture, scale,cords, speed, rotation_angle):
        super().__init__(texture, scale)
        self.center_x, self.center_y = cords
        self.speed = speed
        self.rotation_angle = rotation_angle
        self.m_x , self.m_y = self.center_x//ENV_VAR_DICT['TILE_SIZE'], self.center_y//ENV_VAR_DICT['TILE_SIZE']
        self.key= None

    def update(self, *args, **kwargs):
        self.m_x , self.m_y = self.center_x//ENV_VAR_DICT['TILE_SIZE'], self.center_y//ENV_VAR_DICT['TILE_SIZE']
        super().update()

    def move(self):
        if self.key in KEY_CONFIG:
            self.angle, self.change_x, self.change_y =tuple(
                x * y for x, y in zip(
                    (self.rotation_angle, self.speed, self.speed),
                    KEY_CONFIG[self.key]
                )
            )

    def stop(self):
        if self.center_x % (ENV_VAR_DICT['TILE_SIZE']//2) == 0 and self.center_y %(ENV_VAR_DICT['TILE_SIZE']//2) == 0:
           self.key = None
           super().stop()

    def __str__(self):
        return f'{super().__str__()} {self.angle} {self.m_x} {self.m_y}'
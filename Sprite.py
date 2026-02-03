import random

import arcade
from utils import *

KEY_CONFIG = {
    arcade.key.UP: (-1, 0, 1),
    arcade.key.DOWN: (1, 0, -1),
    arcade.key.LEFT: (2, -1, 0),
    arcade.key.RIGHT:(0, 1, 0)
}

class SpriteTypes:
    def __init__(self, texture, scale, speed, angle):
        self.texture = ENV_VAR_DICT[texture] if texture else "img/pacman.png"
        self.scale = ENV_VAR_DICT[scale] if scale else 1
        self.speed = ENV_VAR_DICT[speed] if speed else 0
        self.angle = ENV_VAR_DICT[angle] if angle else 0

types = {
    "pacman":SpriteTypes("PACMAN_TEXTURE", "PACMAN_SCALE", "PACMAN_MOVE_SPEED", "PACMAN_ANGLE"),
    "r_ghost":SpriteTypes("R_GHOST_TEXTURE", "GHOST_SCALE", "GHOST_MOVE_SPEED", "GHOST_ANGLE"),
    "b_ghost": SpriteTypes("B_GHOST_TEXTURE", "GHOST_SCALE", "GHOST_MOVE_SPEED", "GHOST_ANGLE"),
    "y_ghost": SpriteTypes("Y_GHOST_TEXTURE", "GHOST_SCALE", "GHOST_MOVE_SPEED", "GHOST_ANGLE"),
    "p_ghost": SpriteTypes("P_GHOST_TEXTURE", "GHOST_SCALE", "GHOST_MOVE_SPEED", "GHOST_ANGLE"),
    "wall":SpriteTypes("WALL_TEXTURE", "WALL_SCALE", None, None),
    "coin":SpriteTypes("COIN_TEXTURE", "COIN_SCALE", None, None)
}

class Sprite(arcade.Sprite):
    def __init__(self, character_type, cords):
        self.character_type = character_type
        super().__init__(types[character_type].texture, types[character_type].scale, *cords, types[character_type].angle)
        if character_type == "ghost":
            self.delta_tile = 0
        self.speed = types[character_type].speed
        self.m_x = self.center_x // ENV_VAR_DICT["TILE_SIZE"]
        self.m_y = self.center_y // ENV_VAR_DICT["TILE_SIZE"]
        self.key = None


    def ghost_update(self):
        self.delta_tile += 0.1
        if int(self.delta_tile) == ENV_VAR_DICT["GHOST_DELTA_TIME"]:
            self.delta_tile = 0
            self.key = random.choice([arcade.key.UP,
                                      arcade.key.DOWN,
                                      arcade.key.LEFT,
                                      arcade.key.RIGHT])


    def update(self, delta_time=random.randrange(1,59)/60, *args, **kwargs):
        if self.character_type == "ghost":
            self.ghost_update()

        if self.center_x % 32 - 16 == 0 and self.center_y % 32 - 16 == 0:
            if self.key:
                self.move()
            else:
                self.stop()
        self.m_x , self.m_y = self.center_x//ENV_VAR_DICT["TILE_SIZE"], self.center_y//ENV_VAR_DICT["TILE_SIZE"]
        super().update()


    def move(self):
        if self.key in KEY_CONFIG:
            self.angle, self.change_x, self.change_y =tuple(
                x * y for x, y in zip(
                    (self.angle, self.speed, self.speed),
                    KEY_CONFIG[self.key]
                )
            )


    def stop(self):
        if self.center_x % (ENV_VAR_DICT["TILE_SIZE"]//2) == 0 and self.center_y %(ENV_VAR_DICT["TILE_SIZE"]//2) == 0:
            self.key = None
            super().stop()


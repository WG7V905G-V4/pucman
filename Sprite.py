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
    def __init__(self, texture,  delta_time=None, speed=0, angle=0):
        self.texture = f"img/{texture}.png"
        self.scale = 1
        self.speed = speed
        self.change_angle = angle
        self.delta_time = delta_time

types = {
    "pacman":SpriteTypes("PACMAN_TEXTURE", None, 4, 90),
    "r_ghost":SpriteTypes("R_GHOST_TEXTURE", 100, 4),
    "b_ghost":SpriteTypes("B_GHOST_TEXTURE", 110, 4),
    "y_ghost":SpriteTypes("Y_GHOST_TEXTURE", 120, 4),
    "p_ghost":SpriteTypes("P_GHOST_TEXTURE", 130, 4),
    "wall":SpriteTypes("WALL_TEXTURE"),
    "coin":SpriteTypes("COIN_TEXTURE"),
    "cherry":SpriteTypes("COIN_TEXTURE", 50),
    "powerup":SpriteTypes("COIN_TEXTURE", 6),
    "teleport":SpriteTypes("COIN_TEXTURE")
}

class Sprite(arcade.Sprite):
    def __init__(self, character_type, cords):
        self.character_type = character_type
        x,y =cords
        sprite = types[character_type]
        super().__init__(sprite.texture, sprite.scale, x,y)
        self.angl = sprite.change_angle
        self.speed = sprite.speed
        if sprite.delta_time:
            self.delta_time = sprite.delta_time
        self.m_x = self.center_x // ENV_VAR_DICT["TILE_SIZE"]
        self.m_y = self.center_y // ENV_VAR_DICT["TILE_SIZE"]
        self.key = None
        self.timer=0


    def ghost_update(self):
        if self.delta_time == self.timer:
            self.key = random.choice([arcade.key.UP,
                                      arcade.key.DOWN,
                                      arcade.key.LEFT,
                                      arcade.key.RIGHT])
            self.timer = 0
        self.timer += 1

    def update(self, delta_time=random.randrange(1,59)/60, *args, **kwargs):
        if "ghost" in self.character_type:
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
                    (self.angl, self.speed, self.speed),
                    KEY_CONFIG[self.key]
                )
            )


    def stop(self):
        if self.center_x % (ENV_VAR_DICT["TILE_SIZE"]//2) == 0 and self.center_y %(ENV_VAR_DICT["TILE_SIZE"]//2) == 0:
            self.key = None
            super().stop()

    def teleport(self):
        ...
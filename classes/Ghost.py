import arcade
import math
import random
from .Character import Character
from LevelTools import *


class Ghost(Character):
    def __init__(self, texture, cords):
        self.type = texture[4:-4].lower()
        super().__init__(texture, ENV_VAR_DICT["GHOST_SCALE"], cords, ENV_VAR_DICT['GHOST_MOVE_SPEED'],
                         ENV_VAR_DICT['GHOST_ANGLE'])
        self.normal_texture = self.texture

    def update(self):
        directions = [
            arcade.key.UP,
            arcade.key.DOWN,
            arcade.key.LEFT,
            arcade.key.RIGHT
        ]
        self.key = random.choice(directions)
        super().update()
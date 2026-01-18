import arcade, random
from .Character import Character
from EnvironmentVariables import *

class Ghost(Character):
    def __init__(self, cords):
        super().__init__(GHOST_TEXTURE, cords, GHOST_MOVE_SPEED, GHOST_ROTATION_ANGLE)
        self.ghost_delta_tile = 0

    def update(self):
        self.ghost_delta_tile += 0.1
        if int(self.ghost_delta_tile) == GHOST_DELTA_TIME:
            self.ghost_delta_tile = 0
            self.key = random.choice([arcade.key.UP,
                                                   arcade.key.DOWN,
                                                   arcade.key.LEFT,
                                                   arcade.key.RIGHT,])
        super().update()
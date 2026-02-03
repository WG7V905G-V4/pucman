import arcade, random
from .Character import Character
from LevelTools import *

class Ghost(Character):
    def __init__(self, texture, cords):
        self.type = texture[4:-4].lower()
        super().__init__(texture, ENV_VAR_DICT["GHOST_SCALE"], cords, ENV_VAR_DICT['GHOST_MOVE_SPEED'], ENV_VAR_DICT['GHOST_ANGLE'])
        self.ghost_delta_tile = 0

    def update(self):
        self.ghost_delta_tile += 0.1
        if int(self.ghost_delta_tile) == ENV_VAR_DICT['GHOST_DELTA_TIME']:
            self.ghost_delta_tile = 0
            self.key = random.choice([arcade.key.UP,
                                                   arcade.key.DOWN,
                                                   arcade.key.LEFT,
                                                   arcade.key.RIGHT,])
        super().update()
from .Character import Character
from LevelTools import *

class Pacman(Character):
    def __init__(self, cords):
        super().__init__(ENV_VAR_DICT['PACMAN_TEXTURE'], ENV_VAR_DICT['PACMAN_SCALE'], cords, ENV_VAR_DICT['PACMAN_MOVE_SPEED'], ENV_VAR_DICT['PACMAN_ANGLE'])

    def __str__(self):
        return super().__str__()
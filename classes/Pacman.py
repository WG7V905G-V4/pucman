from .Character import Character
from EnvironmentVariables import *

class Pacman(Character):
    def __init__(self, cords):
        super().__init__(PACMAN_TEXTURE, cords, PACMAN_MOVE_SPEED, PACMAN_ROTATION_ANGLE)



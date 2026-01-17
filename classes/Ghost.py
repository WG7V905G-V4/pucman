from .Character import Character
from EnvironmentVariables import *

class Ghost(Character):
    def __init__(self, cords):
        super().__init__(GHOST_TEXTURE, cords, GHOST_MOVE_SPEED, GHOST_ROTATION_ANGLE)
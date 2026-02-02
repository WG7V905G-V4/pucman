import arcade
from EnvironmentVariables import *

class Teleport(arcade.Sprite):
    def __init__(self, cords):
        x,y = cords
        super().__init__(TELEPORT_TEXTURE, 0.05, x ,y)
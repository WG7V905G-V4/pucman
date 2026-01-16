import arcade
from main import TILE_SIZE
from CharacterClass import Character

class Pacman(Character):
    def __init__(self, center_x, center_y):
        super().__init__("img/pacman.png", center_x, center_y, 1)
        self.rotate

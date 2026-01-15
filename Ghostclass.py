import arcade
import random
from main import TILE_SIZE

class Character(arcade.Sprite):
    def __init__(self, center_x, center_y, speed):
        super().__init__()
        radius = TILE_SIZE // 2 - 2
        self.width = 30
        self.height = 30
        self.center_x = center_x
        self.center_y = center_y
        self.speed = speed
        self.change_x = 0
        self.change_y = 0

class Ghost(Character):
    def __init__(self, center_x, center_y, speed = 0):
        super().__init__(center_x, center_y, speed)
        self.time_to_change_direction = 0

    def pick_new_direction(self):
        direction = [
            (1,0),
            (-1,0),
            (0,-1),
            (0,1),
            (0,0)
        ]

        self.change_x, self.change_y = random.choice(direction)
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self, delta_time = 1/60):
        self.time_to_change_direction -= delta_time
        if self.time_to_change_direction <= 0:
            self.pick_new_direction()
        self.center_x = self.change_x * self.speed
        self.center_x = self.change_x * self.speed
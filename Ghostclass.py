import arcade
import random
class Ghost(arcade.Sprite):
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
import arcade
import random
from CharacterClass import Character

class Ghost(Character):
    def __init__(self, center_x, center_y, speed = 0):
        super().__init__(center_x, center_y, speed)
        self.time_to_change_direction = 0
        texture = arcade.make_circle_texture(self.radius * 2, arcade.color.RED)
        self.texture = texture

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

    def update1(self, delta_time = 1/60):
        self.time_to_change_direction -= delta_time
        if self.time_to_change_direction <= 0:
            self.pick_new_direction()
        self.center_x += self.change_x * self.speed
        self.center_x += self.change_x * self.speed
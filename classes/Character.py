import arcade

class Character(arcade.Sprite):
    def __init__(self, texture, cords, speed, rotation_angle):
        super().__init__(texture, 1.0)
        self.center_x, self.center_y = cords
        self.speed = speed
        self.rotation_angle = rotation_angle

    def move(self, key):
        if key == arcade.key.UP:
            self.angle = self.rotation_angle * -1
            self.change_y = self.speed
            self.change_x = 0
        elif key == arcade.key.DOWN:
            self.angle = self.rotation_angle
            self.change_y = -self.speed
            self.change_x = 0
        elif key == arcade.key.LEFT:
            self.angle = self.rotation_angle *2
            self.change_x = -self.speed
            self.change_y = 0
        elif key == arcade.key.RIGHT:
            self.angle = 0
            self.change_x = self.speed
            self.change_y = 0

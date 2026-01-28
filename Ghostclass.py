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


import arcade
import random
from CharacterClass import Character


class Ghost(Character):
    def __init__(self, center_x, center_y, speed=2):  # Немного увеличим скорость по умолчанию
        super().__init__(center_x, center_y, speed)
        # Текстура круга для привидения
        self.texture = arcade.make_circle_texture(self.radius * 2, arcade.color.RED)

    def follow_target(self, target):
        """
        Метод заставляет привидение менять change_x и change_y
        в зависимости от положения цели (Пакмана).
        """
        # Движение по горизонтали
        if self.center_x < target.center_x:
            self.change_x = 1
        elif self.center_x > target.center_x:
            self.change_x = -1
        else:
            self.change_x = 0

        # Движение по вертикали
        if self.center_y < target.center_y:
            self.change_y = 1
        elif self.center_y > target.center_y:
            self.change_y = -1
        else:
            self.change_y = 0

    def update(self, pacman, delta_time=1 / 60):
        # Вызываем логику преследования
        self.follow_target(pacman)

        # Обновляем координаты (исправлено: добавлена ось Y)
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
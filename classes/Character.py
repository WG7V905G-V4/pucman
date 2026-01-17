import arcade

class Character(arcade.Sprite):
    def __init__(self, texture, cords, speed, rotation_angle):
        super().__init__(texture, 1)
        x, y = cords
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.rotation_angle = rotation_angle


    def move(self, key):
        #TODO: добавить дорисовку пути
        #         (щас позиция в пикселях изза этого скорее всего появится
        #         проблема с тем что пакменом оч трудно попасть
        #         в ширину коридора при повороте)
        # колизию с монетами все равно надо будет реализовывать
        # чтобы это будет проще чем проверять матрицу каждый кадр

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

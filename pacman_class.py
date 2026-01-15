import arcade

class Pacman(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__("img/pacman.png", 0.5)
        self.x = x
        self.y = y
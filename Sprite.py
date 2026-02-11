import random, arcade, csv

def convert(val):
    try:
        return float(val)
    except ValueError:
        return val

with open("SETTINGS/EnvVars.csv", "r") as f:
    ENV_VAR_DICT = {key: convert(val) for key, val in csv.reader(f)}

def cords_to_pixels(cords):
    return tuple([cord * ENV_VAR_DICT["TILE_SIZE"] + ENV_VAR_DICT["TILE_SIZE"] // 2 for cord in cords])

def load_level_from_txt():
    with open("SETTINGS/level.txt", "r", encoding="utf-8") as file:
        return [[sprite(emoji, cords_to_pixels((posx, posy))) for posx, emoji in enumerate(row.strip())] for posy, row in
                enumerate(file.readlines())]

KEY_CONFIG = {
    arcade.key.UP: (-1, 0, 1),
    arcade.key.DOWN: (1, 0, -1),
    arcade.key.LEFT: (2, -1, 0),
    arcade.key.RIGHT:(0, 1, 0)}

class Sprite(arcade.Sprite):
    def __init__(self, type, cords, texture, scale, delta_time, speed, angle):
        self.type = type
        x,y = cords
        super().__init__(f"img/{texture}.png", scale, x,y)
        self.angl = angle
        self.speed = speed
        self.delta_time = delta_time
        self.timer = 0
        self.m_x = self.center_x // ENV_VAR_DICT["TILE_SIZE"]
        self.m_y = self.center_y // ENV_VAR_DICT["TILE_SIZE"]
        self.key = None
        self.points = 10 if "coin" in type else 0
        self.teleportable = True
        self.eatable = False

    def cherry_delete(self):
        self.points = 0
        self.texture = arcade.load_texture("img/BLANK_TEXTURE.png")
    def cherry_add(self):
        self.points = 100
        self.texture = arcade.load_texture("img/CHERRY_TEXTURE.png")


    def ghost_update(self):
        if self.delta_time == self.timer:
            self.key = random.choice([arcade.key.UP,
                                      arcade.key.DOWN,
                                      arcade.key.LEFT,
                                      arcade.key.RIGHT])
            self.timer = 0
        self.timer += 1

    def update(self, delta_time=1/60, *args, **kwargs):
        if "ghost" in self.type:
            self.ghost_update()
        if self.key:
            self.move()
        else:
            self.stop()
        self.m_x , self.m_y = self.center_x//ENV_VAR_DICT["TILE_SIZE"], self.center_y//ENV_VAR_DICT["TILE_SIZE"]
        super().update()

    def move(self):
        if self.center_x % 32 - 16 == 0 and self.center_y % 32 - 16 == 0 and self.key in KEY_CONFIG:
            self.angle, self.change_x, self.change_y =tuple(
                x * y for x, y in zip(
                    (self.angl, self.speed, self.speed),
                    KEY_CONFIG[self.key]
                )
            )

    def stop(self):
        self.key = None
        if self.center_x % (ENV_VAR_DICT["TILE_SIZE"]//2) == 0 and self.center_y %(ENV_VAR_DICT["TILE_SIZE"]//2) == 0:
            super().stop()

    def teleport(self, portal):
        if self.teleportable:
            self.delta_time = portal.delta_time
            self.center_x = portal.center_x
            self.center_y = portal.center_y
            self.teleportable = False

def sprite(emoji, cords):
    types = {"⬜": lambda crds: Sprite("coin", cords, "COIN_TEXTURE", 0.6, None, 0,0),
             "⬛": lambda crds: Sprite("wall", cords, "WALL_TEXTURE",1, None, 0,0),
             "😐": lambda crds: Sprite("pacman", cords, "PACMAN_TEXTURE",1, None, 4, 90),
             "😡": lambda crds: Sprite("r_ghost", cords, "R_GHOST_TEXTURE",1, 100, 4, 0),
             "⭐": lambda crds: Sprite("y_ghost", cords, "Y_GHOST_TEXTURE",1, 110, 3,0),
             "📘": lambda crds: Sprite("b_ghost", cords, "B_GHOST_TEXTURE",1, 120, 2,0),
             "😈": lambda crds: Sprite("p_ghost", cords, "P_GHOST_TEXTURE",1, 130, 3,0),
             "🍎": lambda crds: Sprite("powerup", cords, "COIN_TEXTURE",1.2,None, 0,0),
             "💛": lambda crds: Sprite("teleport", cords, "TELEPORT",1, None, 0,0),
             "🍒": lambda crds: Sprite("cherry", cords, "BLANK_TEXTURE", 1, None, 0,0),
             }
    return types[emoji](cords)


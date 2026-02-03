import arcade
from arcade import check_for_collision_with_lists as collision_lists
from Sprite import Sprite
from utils import *

class PacmanGame(arcade.View):
    def __init__(self, level_matrix, w_s_x=0, w_s_y=0):
        super().__init__()
        self.w, self.h = w_s_x, w_s_y
        self.score = 0
        self.game_over = False
        self.level_matrix = level_matrix
        self.coin = arcade.SpriteList()
        self.ghost = arcade.SpriteList()
        self.wall = arcade.SpriteList()
        self.pacman = None
        self.music = arcade.load_sound(r"C:\qwqwqwq\ьз4\fakemink - Dumb ..mp3", streaming=True)
        arcade.set_background_color(arcade.color.BLACK)

    def append(self, sprite):
        if sprite.character_type == "pacman":
            self.pacman = sprite
            return
        if type == "apple":
            type = "coin"

        type = "ghost" if "ghost" in sprite.character_type else sprite.character_type
        getattr(self, type).append(sprite)

    def stop(self):
        for list_type in ["wall", "coin", "move"]:
            for sprite in getattr(self, list_type):
                sprite.stop()

    def update(self):
        for list_type in ["wall", "coin", "move"]:
            getattr(self, list_type).update()

    def draw(self):
        for list_type in ["wall", "coin", "move"]:
            getattr(self, list_type).draw()

    def setup(self):
        for cord_y, row in enumerate(self.level_matrix):
            for cord_x, item in enumerate(row):
                self.append(Sprite(item, coords_to_pixels((cord_x, cord_y))))

    def on_draw(self):
        self.clear()
        self.draw()
        arcade.draw_text(f"Score: {self.score}", ENV_VAR_DICT['TILE_SIZE']+2, ENV_VAR_DICT['TILE_SIZE']//3,
                         arcade.color.YELLOW, ENV_VAR_DICT['TILE_SIZE']//2)
        if self.game_over and not self.coin:
            arcade.draw_text("YOU WIN", self.w // 2, self.h // 2,
                             arcade.color.GREEN, 50, anchor_x="center")
        if self.game_over and self.coin:
            arcade.draw_text("GAME OVER", self.w // 2, self.h // 2,
                             arcade.color.RED, 50, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if not self.game_over:
            self.pacman.key = key

    def on_update(self, delta_time):
        self.update()
        def collision(sprite):
            sprite.center_x = sprite.m_x * ENV_VAR_DICT['TILE_SIZE'] + ENV_VAR_DICT['TILE_SIZE'] // 2
            sprite.center_y = sprite.m_y * ENV_VAR_DICT['TILE_SIZE'] + ENV_VAR_DICT['TILE_SIZE'] // 2
            sprite.stop()
        for sprite in self.ghost:
            if arcade.check_for_collision_with_list(sprite, self.wall):
                collision(sprite)

        if arcade.check_for_collision_with_list(self.pacman, self.wall):
            collision(self.pacman)

        coin_hit = arcade.check_for_collision_with_list(self.pacman, self.coin)
        for food in coin_hit:
            food.remove_from_sprite_lists()
            self.score += 1

        if not self.coin or arcade.check_for_collision_with_list(self.pacman, self.ghost):
            self.stop()
            self.game_over = True

        if not self.get(["coin"]):
            self.stop()
            self.game_over = True


def main():
    level_matrix = load_level_from_txt()
    w_s_x,w_s_y = len(level_matrix[0])*ENV_VAR_DICT['TILE_SIZE'], len(level_matrix)*ENV_VAR_DICT['TILE_SIZE']
    window = arcade.Window(w_s_x, w_s_y, "PACMAN GAME", resizable=True)
    game = PacmanGame(level_matrix, w_s_x, w_s_y)
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
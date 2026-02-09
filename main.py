from Sprite import *

class PacmanGame(arcade.View):
    def __init__(self, level_matrix, w_s_x=0, w_s_y=0):
        super().__init__()
        self.w, self.h = w_s_x, w_s_y
        self.score = 0
        self.score_text = None
        self.game_over = False

        self.music = arcade.load_sound("music/pacman_back.mp3")

        self.level_matrix = level_matrix
        self.eat_timer = 0

        self.coin = arcade.SpriteList()
        self.ghost = arcade.SpriteList()
        self.move = arcade.SpriteList()
        self.wall = arcade.SpriteList()
        self.teleport = arcade.SpriteList()
        self.cherry = arcade.SpriteList()
        self.powerup = arcade.SpriteList()
        self.pacman = None
        arcade.set_background_color(arcade.color.BLACK)

    def on_key_press(self, key, modifiers):
        if not self.game_over:
            self.pacman.key = key

    def append(self, sprite):
        type = sprite.type
        if "pacman" in type:
            self.pacman = sprite
            type = "move"
        if "ghost" in type:
            self.ghost.append(sprite)
            type = "move"
        getattr(self, type).append(sprite)

    def update(self):
        for list_type in ["wall", "coin", "move", "cherry", "powerup", "teleport"]:
            getattr(self, list_type).update()

    def stop(self):
        for list_type in ["wall", "coin", "move", "cherry", "powerup", "teleport"]:
            for item in getattr(self, list_type):
                item.stop()

    def draw(self):
        for list_type in ["wall", "coin", "move", "cherry", "powerup", "teleport"]:
            getattr(self, list_type).draw()

    def setup(self):
        self.music.play(volume=0.2, loop=True)
        for row in self.level_matrix:
            for item in row:
                self.append(item)

    def on_draw(self):
        self.clear()
        self.draw()
        arcade.Text(f"Score: {self.score}",
                    ENV_VAR_DICT['TILE_SIZE'] + 2,
                    ENV_VAR_DICT['TILE_SIZE'] // 3,
                    arcade.color.YELLOW,
                    ENV_VAR_DICT['TILE_SIZE'] // 2).draw()

        if self.game_over:
            arcade.Text("YOU WIN" if not self.coin else "YOU LOST",
                        self.w // 2,
                        self.h // 2,
                        arcade.color.GREEN if not self.coin else arcade.color.RED,
                        50,
                        anchor_x="center").draw()

    def on_update(self, delta_time):
        self.update()
        for item in self.move:
            if arcade.check_for_collision_with_list(item, self.wall):
                item.center_x = item.m_x * ENV_VAR_DICT['TILE_SIZE'] + ENV_VAR_DICT['TILE_SIZE'] // 2
                item.center_y = item.m_y * ENV_VAR_DICT['TILE_SIZE'] + ENV_VAR_DICT['TILE_SIZE'] // 2
                item.stop()
            if self.teleport[0].delta_time and arcade.check_for_collision(item, self.teleport[0]):
                self.pacman.teleport(self.teleport[1])
            if self.teleport[1].delta_time and arcade.check_for_collision(item, self.teleport[1]):
                self.pacman.teleport(self.teleport[0])
            if not arcade.check_for_collision_with_list(item, self.teleport):
                for i in self.teleport:
                    i.delta_time = True

        coin_hit = arcade.check_for_collision_with_lists(self.pacman, self.coin, self.cherry)
        for coin in coin_hit:
            arcade.play_sound(arcade.load_sound("music/coin.mp3"), volume=0.2)
            coin.remove_from_sprite_lists()
            self.score += coin.points

        if self.score%70 == 0:
            for i in self.cherry:
                i.update_cherry()




        if not self.coin or arcade.check_for_collision_with_list(self.pacman, self.ghost):
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
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
        self.music.play(volume=0.2, loop=True)

    def on_key_press(self, key, modifiers):
        if not self.game_over:
            self.pacman.key = key

    def setup(self):
        for row in self.level_matrix:
            for item in row:
                type = item.type
                if "pacman" in type:
                    self.pacman = item
                    type = "move"
                if "ghost" in type:
                    self.ghost.append(item)
                    type = "move"
                getattr(self, type).append(item)

    def on_draw(self):
        self.clear()
        for list_type in ["wall", "coin", "move", "cherry", "powerup", "teleport"]:
            getattr(self, list_type).draw()
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

    def stop(self):
        for list_type in ["wall", "coin", "move", "cherry", "powerup", "teleport"]:
            for item in getattr(self, list_type):
                item.stop()

    def update(self):
        for list_type in ["wall", "coin", "move", "cherry", "powerup", "teleport"]:
            getattr(self, list_type).update()

    def on_update(self, delta_time):
        self.update()
        for item in self.move:

            #WALL COLLISION
            if arcade.check_for_collision_with_list(item, self.wall):
                item.center_x, item.center_y = cords_to_pixels((item.m_x, item.m_y))
                item.stop()

            #TELEPORT
            if arcade.check_for_collision(item, self.teleport[0]):
                item.teleport(self.teleport[1])
            if arcade.check_for_collision(item, self.teleport[1]):
                item.teleport(self.teleport[0])
            if not arcade.check_for_collision_with_list(item, self.teleport):
                item.teleportable = True

        #COIN
        coin_hit = arcade.check_for_collision_with_list(self.pacman, self.coin)
        for coin in coin_hit:
            arcade.play_sound(arcade.load_sound("music/coin.mp3"), volume=0.2)
            coin.remove_from_sprite_lists()
            self.score += coin.points

        #CHERRY
        if self.score%70==0 and self.score>70 and self.cherry[0].points==0:
            self.cherry[0].cherry_add()
        if arcade.check_for_collision_with_list(self.pacman, self.cherry):
            self.score+=self.cherry[0].points
            self.cherry[0].cherry_delete()

        #POWER UP
        hit_powerups = arcade.check_for_collision_with_list(self.pacman, self.powerup)
        for powerup in hit_powerups:
            powerup.remove_from_sprite_lists()
            for ghost in self.ghost:
                ghost.texture = arcade.load_texture("img/GHOST_ALT.png")
                self.eat_timer = 360

        if self.eat_timer > 0:
            self.eat_timer -= 1

        if self.eat_timer == 0:
            for ghost in self.ghost:
                ghost.texture = arcade.load_texture(f"img/{ghost.type.upper()}_TEXTURE.png")

        #GAME END
        if not self.coin or arcade.check_for_collision_with_list(self.pacman, self.ghost):
            self.stop()
            self.game_over = True



def main():
    level_matrix = load_level_from_txt()
    w_s_x,w_s_y = cords_to_pixels((len(level_matrix[0]), len(level_matrix)))
    window = arcade.Window(w_s_x-16, w_s_y-16, "PACMAN GAME", resizable=True)
    game = PacmanGame(level_matrix, w_s_x, w_s_y)
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
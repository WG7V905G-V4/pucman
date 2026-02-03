from sys import flags

import arcade
from LevelTools import *
from classes.Ghost import Ghost
from classes.Pacman import Pacman
from classes.Wall import Wall
from classes.Coin import Coin
from classes.Apple import Apple
import time
from classes.Teleport import Teleport

TILE = ENV_VAR_DICT["TILE_SIZE"]
class PacmanGame(arcade.View):
    def __init__(self, level_matrix, w_s_x=0, w_s_y=0):
        self.level_matrix = level_matrix
        self.w, self.h = w_s_x, w_s_y

        super().__init__()
        self.score = 0
        self.game_over = False

        self.wall_list =arcade.SpriteList()
        self.coin_list =arcade.SpriteList()
        self.teleport_list = arcade.SpriteList()
        self.player = None
        self.moving_sprites = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.key = None
        self.fruit_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()

        self.eat_ghost_mode_on = False
        self.time_for_eat_mode = 0
        self.eat_time = 0
        self.flag_tep = False
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        for i_row, row in enumerate(self.level_matrix):
            for i_col, col in enumerate(self.level_matrix[i_row]):
                if col == "coin":
                    self.coin_list.append(Coin(coords_to_pixels((i_col, i_row))))
                elif col == "wall":
                    self.wall_list.append(Wall(coords_to_pixels((i_col, i_row))))
                elif "ghost" in col:
                    ghost = Ghost(ENV_VAR_DICT[col.upper()+"_TEXTURE"], coords_to_pixels((i_col, i_row)))
                    self.ghost_list.append(ghost)
                    self.moving_sprites.append(ghost)
                elif col == "pacman":
                    self.player = Pacman(coords_to_pixels((i_col, i_row)))
                    self.moving_sprites.append(self.player)
                elif col == 'apple':
                    self.apple_list.append(Apple(coords_to_pixels((i_col, i_row))))
                elif col == "teleport":
                    self.teleport_list.append(Teleport(coords_to_pixels((i_col, i_row))))


    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.coin_list.draw()
        self.teleport_list.draw()
        self.apple_list.draw()
        self.moving_sprites.draw()

        arcade.draw_text(f"Score: {self.score}", TILE_SIZE+2, TILE_SIZE//3,
                         arcade.color.YELLOW, TILE_SIZE//2)
        if self.game_over and not self.coin_list:
            arcade.draw_text("YOU WIN", self.w // 2, self.h // 2,
                             arcade.color.GREEN, 50, anchor_x="center")

        if self.game_over and self.coin_list:
            arcade.draw_text("GAME OVER", self.w // 2, self.h // 2,
                             arcade.color.RED, 50, anchor_x="center")



    def on_key_press(self, key, modifiers):
        if not self.game_over:
            self.player.key = key

    def on_update(self, delta_time):
        if self.eat_ghost_mode_on:
            cur_time = time.time()
            if cur_time - self.eat_time >= self.time_for_eat_mode:
                self.eat_ghost_mode_on = False
                self.time_for_eat_mode = 0
                for ghost in self.ghost_list:
                    ghost.texture = arcade.load_texture(ENV_VAR_DICT[ghost.type.upper()+"_TEXTURE"])

        for sprite in self.moving_sprites:
            if sprite.center_x % 32 - 16 == 0 and sprite.center_y % 32 -16 == 0:
                if sprite.key is None:
                    sprite.stop()
                else:
                    sprite.move()

        for ghost in self.ghost_list:
            # Передаем игрока и стены для умного поиска пути
            ghost.update(self.player, self.wall_list)

            # --- ИСПРАВЛЕНИЕ НИЖЕ ---

            # 1. Если призрак врезался в СТЕНУ -> стоп и возврат на клетку
            if arcade.check_for_collision_with_list(ghost, self.wall_list):
                ghost.center_x = ghost.m_x * TILE_SIZE + 16
                ghost.center_y = ghost.m_y * TILE_SIZE + 16
                ghost.stop()

            # 2. Если призрак попал в ТЕЛЕПОРТ (если нужно, чтобы они телепортировались)
            # Если не хотите, чтобы призраки телепортировались, уберите этот блок
            if arcade.check_for_collision_with_list(ghost, self.teleport_list):
                # Логика телепортации призраков (если нужна)
                pass

                # ЗАМЕТЬТЕ: Мы УБРАЛИ проверку (ghost, self.ghost_list)

        # ... (дальше код для player)





        if arcade.check_for_collision_with_list(player:=self.player, self.wall_list):
            player.center_x = player.m_x * TILE_SIZE + 16
            player.center_y = player.m_y * TILE_SIZE + 16
            player.stop()

        if self.flag_tep and arcade.check_for_collision(self.player, self.teleport_list[0]):
            self.player.center_x, self.player.center_y = self.teleport_list[1].center_x, self.teleport_list[1].center_y
            self.flag_tep = False
            print(self.player.center_x, self.player.center_y)

        if self.flag_tep and arcade.check_for_collision(self.player, self.teleport_list[1]):
            self.player.center_x, self.player.center_y = self.teleport_list[0].center_x, self.teleport_list[0].center_y
            print(self.player.center_x, self.player.center_y)
            self.flag_tep = False
        if not arcade.check_for_collision_with_list(self.player, self.teleport_list):
            self.flag_tep = True


        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        apples_hit_list = arcade.check_for_collision_with_list(self.player, self.apple_list)

        for apple in apples_hit_list:
            apple.remove_from_sprite_lists()
            self.time_for_eat_mode += 6
            for ghost in self.ghost_list:
                ghost.texture = arcade.load_texture(ENV_VAR_DICT["EATABLE"])
            self.eat_ghost_mode_on = True
            self.eat_time = time.time()



        if not self.coin_list:
            for sprite in self.moving_sprites:
                sprite.stop()
            self.game_over = True

        if arcade.check_for_collision_with_list(self.player, self.ghost_list):
            if self.eat_ghost_mode_on:
                ghost_hit_list = arcade.check_for_collision_with_list(self.player, self.ghost_list)
                for ghost in ghost_hit_list:
                    ghost.remove_from_sprite_lists()
            else:
                for sprite in self.moving_sprites:
                    sprite.stop()
                self.game_over = True
        self.player.update()



def main():
    level_matrix = load_level_from_txt()
    w_s_x, w_s_y = len(level_matrix[0]) * ENV_VAR_DICT['TILE_SIZE'], len(level_matrix) * ENV_VAR_DICT['TILE_SIZE']
    window = arcade.Window(w_s_x, w_s_y, "PACMAN GAME", resizable=True)
    game = PacmanGame(level_matrix, w_s_x, w_s_y)

    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
import arcade
from LevelTools import *
from classes.Ghost import Ghost
from classes.Pacman import Pacman
from classes.Wall import Wall
from classes.Coin import Coin


class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.game_over = False

        self.wall_list =arcade.SpriteList()
        self.coin_list =arcade.SpriteList()
        self.player = None
        self.moving_sprites = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.key = None
        self.fruit_list = arcade.SpriteList()

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        level_matrix = generate_maze_with_cycles(WINDOW_WIDTH // TILE_SIZE, WINDOW_HEIGHT // TILE_SIZE, MAZE_CYCLE_GENERATION)
        set_pacman_position(level_matrix)
        set_ghost_cage(level_matrix)

        for row in range(len(level_matrix)):
            for col in range(len(level_matrix[row])):
                if level_matrix[row][col] == 0:
                    self.coin_list.append(Coin(coords_to_pixels((col, row))))
                elif level_matrix[row][col] == 1:
                    self.wall_list.append(Wall(coords_to_pixels((col, row))))
                elif level_matrix[row][col] == 2:
                    ghost = Ghost(coords_to_pixels((col, row)))
                    self.ghost_list.append(ghost)
                    self.moving_sprites.append(ghost)
                elif level_matrix[row][col] == 3:
                    self.player = Pacman(coords_to_pixels((col, row)))
                    self.moving_sprites.append(self.player)


    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.coin_list.draw()
        self.moving_sprites.draw()

        arcade.draw_text(f"Score: {self.score}", TILE_SIZE+2, TILE_SIZE//3,
                         arcade.color.YELLOW, TILE_SIZE//2)
        if self.game_over and not self.coin_list:
            arcade.draw_text("YOU WIN", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.GREEN, 50, anchor_x="center")

        if self.game_over and self.coin_list:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.RED, 50, anchor_x="center")



    def on_key_press(self, key, modifiers):
        if not self.game_over:
            self.player.key = key

    def on_update(self, delta_time):
        for sprite in self.moving_sprites:
            if sprite.center_x % 32 - 16 == 0 and sprite.center_y % 32 -16 == 0:
                if sprite.key is None:
                    sprite.stop()
                else:
                    sprite.move()

            if type(sprite) == Ghost:
                if arcade.check_for_collision_with_list(sprite, self.ghost_list):
                    sprite.center_x = sprite.m_x*TILE_SIZE+16
                    sprite.center_y = sprite.m_y*TILE_SIZE+16
                    sprite.stop()


            if arcade.check_for_collision_with_list(sprite, self.wall_list):
                sprite.center_x = sprite.m_x*TILE_SIZE+16
                sprite.center_y = sprite.m_y*TILE_SIZE+16
                sprite.stop()


        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1



        if not self.coin_list:
            for sprite in self.moving_sprites:
                sprite.stop()
            self.game_over = True

        if arcade.check_for_collision_with_list(self.player, self.ghost_list):
            for sprite in self.moving_sprites:
                sprite.stop()
            self.game_over = True


        for sprite in self.moving_sprites:
            sprite.update()

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "PACMAN GAME")
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
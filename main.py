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
        self.ghost = None
        self.player = None
        self.moving_sprites = arcade.SpriteList()
        self.ghost_move_timer = 0
        self.key = None
        self.physics_engines = []

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        level_matrix = generate_maze_with_cycles(WINDOW_WIDTH // TILE_SIZE, WINDOW_HEIGHT // TILE_SIZE, 0)
        set_pacman_position(level_matrix)
        set_ghost_cage(level_matrix)

        for row in range(len(level_matrix)):
            for col in range(len(level_matrix[row])):
                if level_matrix[row][col] == 0:
                    self.coin_list.append(Coin(coords_to_pixels((col, row))))
                elif level_matrix[row][col] == 1:
                    self.wall_list.append(Wall(coords_to_pixels((col, row))))
                elif level_matrix[row][col] == 2:
                    self.ghost = Ghost(coords_to_pixels((col, row)))
                    self.moving_sprites.append(self.ghost)
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
            self.key = key

    def on_key_release(self, key, modifiers):
        if self.key == key:
            self.key = None

    def on_update(self, delta_time):

        if self.player.center_x % 32 - 16 == 0 and self.player.center_y % 32 -16 == 0:
            if self.key is None:
                self.player.stop()
            else:
                self.player.move(self.key)

        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x = self.player.m_x*TILE_SIZE+16
            self.player.center_y = self.player.m_y*TILE_SIZE+16
            self.player.stop()
            self.key = None



        if self.ghost.center_x % 32 - 16 == 0 and self.ghost.center_y % 32 -16 == 0:
            if self.key is None:
                self.ghost.stop()
            else:
                self.ghost_move_timer += delta_time
                if self.ghost_move_timer >= 0.2:
                    self.ghost_move_timer = 0
                    self.ghost.move(random.choice([arcade.key.UP,
                                               arcade.key.DOWN,
                                               arcade.key.LEFT,
                                               arcade.key.RIGHT]))

        if arcade.check_for_collision_with_list(self.ghost, self.wall_list):
            self.ghost.center_x = self.ghost.m_x*TILE_SIZE+16
            self.ghost.center_y = self.ghost.m_y*TILE_SIZE+16
            self.ghost.stop()


        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        if not self.coin_list:
            self.player.stop()
            self.ghost.stop()
            self.game_over = True


        if arcade.check_for_collision(self.player, self.ghost):
            self.player.stop()
            self.ghost.stop()
            self.game_over = True


        self.player.update()
        self.ghost.update()


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "PACMAN GAME")
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
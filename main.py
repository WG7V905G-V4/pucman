import arcade

from EnvironmentVariables import *
from LevelTools import *
from classes.Ghost import Ghost
from classes.Pacman import Pacman
from classes.Wall import Wall
from classes.Coin import Coin

class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.wall_list =arcade.SpriteList()
        self.coin_list =arcade.SpriteList()
        self.ghost = None
        self.player = None
        self.game_over = False
        self.ghost_move_timer = 0
        self.score = 0


    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        level_matrix = generate_maze_with_cycles(WINDOW_WIDTH // TILE_SIZE, WINDOW_HEIGHT // TILE_SIZE, 0)
        self.player = (Pacman(coords_to_pixels(set_pacman_position(level_matrix))))
        self.ghost = (Ghost(coords_to_pixels(set_pacman_position(level_matrix))))
        for row in range(len(level_matrix)):
            for col in range(len(level_matrix[row])):
                if level_matrix[row][col] == 1:
                    self.wall_list.append(Wall(coords_to_pixels((col, row))))
                else:
                    self.coin_list.append(Coin(coords_to_pixels((col, row))))

        debug_matrix(level_matrix)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost.draw()
        self.player.draw()

        arcade.draw_text(f"Score: {self.score}", 10, WINDOW_HEIGHT - 30,
                         arcade.color.WHITE, 20)

        if self.game_over:
            arcade.draw_text("GAME OVER!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.RED, 50, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if not self.game_over:
            self.player.move(key)

    def on_key_release(self, key, modifiers):
        if not self.game_over:
            self.player.stop()

    def on_update(self, delta_time):
        self.wall_list.update()
        self.coin_list.update()
        self.player.update()

        self.ghost_move_timer += delta_time
        if self.ghost_move_timer >= 0.2:
            self.ghost_move_timer = 0

            old_ghost_x = self.ghost.center_x
            old_ghost_y = self.ghost.center_y

            self.ghost.move(random.choice([arcade.key.UP,
                                           arcade.key.DOWN,
                                           arcade.key.LEFT,
                                           arcade.key.RIGHT]))
            self.ghost.update()


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "PACMAN GAME")
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
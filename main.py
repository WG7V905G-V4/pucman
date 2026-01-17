import arcade
import random
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

        self.moving_sprites = arcade.SpriteList()
        self.ghost = None
        self.player = None
        self.ghost_move_timer = 0

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
        for item in self.moving_sprites:
            self.physics_engines.append(arcade.PhysicsEngineSimple(item,self.wall_list))


        debug_matrix(level_matrix)


    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()

        self.moving_sprites.draw()



        arcade.draw_text(f"Score: {self.score}", TILE_SIZE+2, TILE_SIZE//3,
                         arcade.color.WHITE, TILE_SIZE//2)
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
        if arcade.check_for_collision(self.player, self.ghost):
            self.player.stop()
            self.ghost.stop()
            self.game_over = True
        for engine in self.physics_engines:
            engine.update()

        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.stop()

        self.player.update()
        self.ghost.update()

        self.ghost_move_timer += delta_time
        if self.ghost_move_timer >= 0.2:
            self.ghost_move_timer = 0
            self.ghost.move(random.choice([arcade.key.UP,
                                           arcade.key.DOWN,
                                           arcade.key.LEFT,
                                           arcade.key.RIGHT]))


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "PACMAN GAME")
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
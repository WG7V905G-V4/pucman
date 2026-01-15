import LEVELTOOLS
import arcade


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 32
LEVEL_MATRIX = LEVELTOOLS.generate_maze_with_cycles(WINDOW_WIDTH//TILE_SIZE, WINDOW_HEIGHT//TILE_SIZE, 0)
LEVELTOOLS.set_pacman_position(LEVEL_MATRIX)
LEVELTOOLS.set_ghost_cage(LEVEL_MATRIX)

LEVELTOOLS.debug_matrix(LEVEL_MATRIX)

class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.wall_list =arcade.SpriteList()
        self.coin_list =arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player = None
        self.game_over = False
        self.background_color = arcade.color.BLACK
        self.start_y, self.start_x = LEVELTOOLS.set_pacman_position(LEVEL_MATRIX)

    def setup(self):
        """Инициализация мира игры (один раз перед стартом или при рестарте)."""
        self.score = 0
        arcade.set_background_color(arcade.color.BLACK)

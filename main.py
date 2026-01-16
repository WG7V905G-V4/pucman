from Wall import *
import arcade
from LEVELTOOLS import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 32



class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.wall_list =arcade.SpriteList()
        self.coin_list =arcade.SpriteList()
        #self.ghost_list = arcade.SpriteList()
        self.player_list = Pacman(x,y)
        #self.player = None
        self.game_over = False
        self.background_color = arcade.color.BLACK
        #self.start_y, self.start_x = 0,0

    def setup(self):
        """Инициализация мира игры при старте"""
        # генерация лабиринта
        LEVEL_MATRIX = generate_maze_with_cycles(WINDOW_WIDTH // TILE_SIZE, WINDOW_HEIGHT // TILE_SIZE, 0)
        set_ghost_cage(LEVEL_MATRIX)  # отчистка центра, чтобы разместить призрака
        debug_matrix(LEVEL_MATRIX)  # отрисовка лабиринта в консоль для дебагинга

        # color setup
        arcade.set_background_color(self.background_color)

        #wall setup
        for row in range(len(LEVEL_MATRIX)):
            for col in range(len(LEVEL_MATRIX[row])):
                if LEVEL_MATRIX[row][col] == 1:
                    self.wall_list.append(BlueWall(coords_to_pixels(col, TILE_SIZE), coords_to_pixels(row, TILE_SIZE)))

        #pucman setup
        self.start_y, self.start_x = set_pacman_position(LEVEL_MATRIX)


    def on_draw(self):
        """Arcade сам вызывает это каждый кадр."""
        self.clear()

    def on_key_press(self, key, modifiers):
        """Пример: по пробелу увеличиваем счёт."""
        if key == arcade.key.UP:
            self.score += 1

def main():
    # 1. Создаём окно
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "PACMAN GAME")

    # 2. Создаём объект игры (View)
    game = PacmanGame()

    # 3. Инициализируем мир
    game.setup()

    # 4. Показываем View в окне
    window.show_view(game)

    # 5. Запускаем игровой цикл
    arcade.run()


if __name__ == "__main__":
    main()
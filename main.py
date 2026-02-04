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

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
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

        # Для A* алгоритма
        self.barrier_list = None
        self.ghost_paths = {}  # Словарь для хранения путей каждого призрака

        # sounds and music
        self.coin_sound = arcade.load_sound("music/coin_sound.wav")
        self.apple_sound = arcade.load_sound("music/apple_sound.wav")
        self.win_sound = arcade.load_sound("music/win_sound.wav")
        self.lose_sound = arcade.load_sound("music/lose_sound.wav")

    def setup(self):
        for i_row, row in enumerate(self.level_matrix):
            for i_col, col in enumerate(self.level_matrix[i_row]):
                if col == "coin":
                    self.coin_list.append(Coin(coords_to_pixels((i_col, i_row))))
                elif col == "wall":
                    self.wall_list.append(Wall(coords_to_pixels((i_col, i_row))))
                elif "ghost" in col:
                    ghost = Ghost(ENV_VAR_DICT[col.upper() + "_TEXTURE"], coords_to_pixels((i_col, i_row)))
                    self.ghost_list.append(ghost)
                    self.moving_sprites.append(ghost)
                    # Инициализируем путь для каждого призрака
                    self.ghost_paths[ghost] = None
                elif col == "pacman":
                    self.player = Pacman(coords_to_pixels((i_col, i_row)))
                    self.moving_sprites.append(self.player)
                elif col == 'apple':
                    self.apple_list.append(Apple(coords_to_pixels((i_col, i_row))))
                elif col == "teleport":
                    self.teleport_list.append(Teleport(coords_to_pixels((i_col, i_row))))

        # Создаем AStarBarrierList после того, как все стены загружены
        # Используем первого призрака для расчета размеров (все призраки одинакового размера)
        if self.ghost_list:
            ghost_example = self.ghost_list[0]

            # Границы игрового поля
            playing_field_left = 0
            playing_field_right = len(self.level_matrix[0]) * TILE_SIZE
            playing_field_bottom = 0
            playing_field_top = len(self.level_matrix) * TILE_SIZE

            # Создаем барьерный список для A*
            self.barrier_list = arcade.AStarBarrierList(
                ghost_example,
                self.wall_list,
                TILE_SIZE,  # Размер сетки
                playing_field_left,
                playing_field_right,
                playing_field_bottom,
                playing_field_top
            )

    def calculate_ghost_path(self, ghost):
        """Вычислить путь для призрака к игроку используя встроенный A*"""
        if self.barrier_list is None or self.player is None:
            return None

        # Получаем стартовую и конечную точки
        start_point = (ghost.center_x, ghost.center_y)
        end_point = (self.player.center_x, self.player.center_y)

        # Вычисляем путь с помощью встроенной функции Arcade
        # diagonal_movement=False для движения только по 4 направлениям (как в классическом Pacman)
        path = arcade.astar_calculate_path(
            start_point,
            end_point,
            self.barrier_list,
            diagonal_movement=False
        )

        return path

    def get_next_direction(self, ghost):
        """Определить следующее направление движения для призрака"""
        # Проверяем, находится ли призрак в центре клетки
        is_centered = (ghost.center_x % TILE_SIZE - 16 == 0 and
                       ghost.center_y % TILE_SIZE - 16 == 0)

        if not is_centered:
            return None

        # Если режим поедания призраков включен - убегаем от игрока
        if self.eat_ghost_mode_on:
            # Простая логика убегания: двигаемся в противоположном направлении
            dx = ghost.center_x - self.player.center_x
            dy = ghost.center_y - self.player.center_y

            if abs(dx) > abs(dy):
                return arcade.key.RIGHT if dx > 0 else arcade.key.LEFT
            else:
                return arcade.key.UP if dy > 0 else arcade.key.DOWN

        # Обычный режим: преследование
        # Получаем или пересчитываем путь
        if self.ghost_paths[ghost] is None or len(self.ghost_paths[ghost]) <= 1:
            self.ghost_paths[ghost] = self.calculate_ghost_path(ghost)

        # Если путь найден, двигаемся по нему
        if self.ghost_paths[ghost] and len(self.ghost_paths[ghost]) > 1:
            # Берем следующую точку в пути (первая точка - это текущая позиция)
            next_point = self.ghost_paths[ghost][1]

            # Определяем направление к следующей точке
            dx = next_point[0] - ghost.center_x
            dy = next_point[1] - ghost.center_y

            # Убираем первую точку из пути
            self.ghost_paths[ghost].pop(0)

            # Возвращаем направление движения
            if abs(dx) > abs(dy):
                return arcade.key.RIGHT if dx > 0 else arcade.key.LEFT
            else:
                return arcade.key.UP if dy > 0 else arcade.key.DOWN

        return None

    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.coin_list.draw()
        self.teleport_list.draw()
        self.apple_list.draw()
        self.moving_sprites.draw()

        arcade.draw_text(f"Score: {self.score}", TILE_SIZE + 2, TILE_SIZE // 3,
                         arcade.color.YELLOW, TILE_SIZE // 2)

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
        if self.game_over:
            return

        if self.eat_ghost_mode_on:
            cur_time = time.time()
            if cur_time - self.eat_time >= self.time_for_eat_mode:
                self.eat_ghost_mode_on = False
                self.time_for_eat_mode = 0
                for ghost in self.ghost_list:
                    ghost.texture = arcade.load_texture(ENV_VAR_DICT[ghost.type.upper() + "_TEXTURE"])

        for sprite in self.moving_sprites:
            if sprite.center_x % 32 - 16 == 0 and sprite.center_y % 32 - 16 == 0:
                if sprite.key is None:
                    sprite.stop()
                else:
                    sprite.move()

        # Обновление призраков с A* pathfinding
        for ghost in self.ghost_list:
            # Получаем направление для призрака используя A*
            direction = self.get_next_direction(ghost)
            if direction:
                ghost.key = direction

            # Обновляем позицию призрака
            ghost.update(self.player, self.wall_list)

            # Проверка коллизии со стеной
            if arcade.check_for_collision_with_list(ghost, self.wall_list):
                ghost.center_x = ghost.m_x * TILE_SIZE + 16
                ghost.center_y = ghost.m_y * TILE_SIZE + 16
                ghost.stop()
                # Сбрасываем путь при столкновении
                self.ghost_paths[ghost] = None

            # Телепортация призраков (если нужна)
            if arcade.check_for_collision_with_list(ghost, self.teleport_list):
                pass

        # Обновление игрока
        if arcade.check_for_collision_with_list(player := self.player, self.wall_list):
            player.center_x = player.m_x * TILE_SIZE + 16
            player.center_y = player.m_y * TILE_SIZE + 16
            player.stop()

        # Телепортация игрока
        if self.flag_tep and arcade.check_for_collision(self.player, self.teleport_list[0]):
            self.player.center_x, self.player.center_y = self.teleport_list[1].center_x, self.teleport_list[1].center_y
            self.flag_tep = False

        if self.flag_tep and arcade.check_for_collision(self.player, self.teleport_list[1]):
            self.player.center_x, self.player.center_y = self.teleport_list[0].center_x, self.teleport_list[0].center_y
            self.flag_tep = False

        if not arcade.check_for_collision_with_list(self.player, self.teleport_list):
            self.flag_tep = True

        # Сбор монет
        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.coin_sound)

        # Сбор яблок
        apples_hit_list = arcade.check_for_collision_with_list(self.player, self.apple_list)
        for apple in apples_hit_list:
            apple.remove_from_sprite_lists()
            self.time_for_eat_mode += 6
            arcade.play_sound(self.apple_sound)
            for ghost in self.ghost_list:
                ghost.texture = arcade.load_texture(ENV_VAR_DICT["EATABLE"])
            self.eat_ghost_mode_on = True
            self.eat_time = time.time()
            # Сбрасываем пути всех призраков при активации режима поедания
            for ghost in self.ghost_list:
                self.ghost_paths[ghost] = None

        # Победа
        if not self.coin_list and not self.game_over:
            for sprite in self.moving_sprites:
                sprite.stop()
            self.game_over = True
            arcade.play_sound(self.win_sound)

        # Столкновение с призраками
        if arcade.check_for_collision_with_list(self.player, self.ghost_list) and not self.game_over:
            if self.eat_ghost_mode_on:
                ghost_hit_list = arcade.check_for_collision_with_list(self.player, self.ghost_list)
                for ghost in ghost_hit_list:
                    ghost.remove_from_sprite_lists()
                    # Удаляем путь съеденного призрака
                    if ghost in self.ghost_paths:
                        del self.ghost_paths[ghost]
            else:
                for sprite in self.moving_sprites:
                    sprite.stop()
                self.game_over = True
                arcade.play_sound(self.lose_sound)

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
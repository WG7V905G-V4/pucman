import arcade
import math
import random
from .Character import Character
from LevelTools import *


class Ghost(Character):
    def __init__(self, texture, cords):
        self.type = texture[4:-4].lower()
        super().__init__(texture, ENV_VAR_DICT["GHOST_SCALE"], cords, ENV_VAR_DICT['GHOST_MOVE_SPEED'],
                         ENV_VAR_DICT['GHOST_ANGLE'])
        self.normal_texture = self.texture

    def update(self, player, wall_list):
        tile_size = ENV_VAR_DICT['TILE_SIZE']  # Обычно 32
        speed = ENV_VAR_DICT['GHOST_MOVE_SPEED']

        # 1. Проверяем, находимся ли мы ровно в центре клетки (перекрестке)
        # Допуск (tolerance) чуть больше скорости, чтобы не проскочить
        in_grid_x = abs((self.center_x - tile_size // 2) % tile_size) < speed
        in_grid_y = abs((self.center_y - tile_size // 2) % tile_size) < speed

        if in_grid_x and in_grid_y:
            # Принудительно ставим призрака в центр, чтобы он поворачивал идеально ровно
            self.center_x = (self.center_x // tile_size) * tile_size + tile_size // 2
            self.center_y = (self.center_y // tile_size) * tile_size + tile_size // 2

            directions = [
                (arcade.key.UP, 0, 1),
                (arcade.key.DOWN, 0, -1),
                (arcade.key.LEFT, -1, 0),
                (arcade.key.RIGHT, 1, 0)
            ]

            best_key = None
            min_dist = float('inf')
            possible_moves = []

            # Перебираем все 4 стороны
            for key, dx, dy in directions:
                # А. Запрещаем разворот на 180 градусов (чтобы призрак не дергался туда-сюда)
                # Если мы идем вправо (change_x > 0), мы не можем пойти влево (dx = -1)
                if self.change_x > 0 and dx == -1: continue
                if self.change_x < 0 and dx == 1: continue
                if self.change_y > 0 and dy == -1: continue
                if self.change_y < 0 and dy == 1: continue

                # Б. Проверка СТЕНЫ
                # Предсказываем координаты следующей клетки
                future_x = self.center_x + (dx * tile_size)
                future_y = self.center_y + (dy * tile_size)

                hit_wall = False
                # Пробегаем по списку стен и смотрим, попадает ли туда будущая точка
                for wall in wall_list:
                    if wall.left < future_x < wall.right and wall.bottom < future_y < wall.top:
                        hit_wall = True
                        break

                # Если стены нет, добавляем этот ход в список возможных
                if not hit_wall:
                    dist = math.sqrt((future_x - player.center_x) ** 2 + (future_y - player.center_y) ** 2)
                    possible_moves.append((key, dist))

            # В. Выбираем лучший ход из возможных
            if possible_moves:
                # Сортируем ходы по дистанции (от меньшей к большей)
                possible_moves.sort(key=lambda x: x[1])

                # Берем самый короткий путь (первый элемент)
                best_key = possible_moves[0][0]
                self.key = best_key
            else:
                # Если зашли в тупик (все ходы блокированы или разворот запрещен),
                # разрешаем просто продолжить движение или ждать следующего цикла
                pass

        super().update()
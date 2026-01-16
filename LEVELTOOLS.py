import random

def generate_maze_with_cycles(width, height, cycle_percent=15):
    """
    Генерирует лабиринт с множественными путями без изолированных областей.

    Args:
        width: ширина лабиринта (нечётное число)
        height: высота лабиринта (нечётное число)
        cycle_percent: процент стен для удаления (0-100), создаёт циклы

    Returns:
        matrix: двумерный список, где 0 = путь, 1 = стена
    """

    # Убеждаемся что размеры нечётные
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    # ЭТАП 1: Генерация идеального лабиринта (алгоритм Прима)
    matrix = [[1 for _ in range(width)] for _ in range(height)]
    start_x, start_y = 1, 1
    matrix[start_y][start_x] = 0

    # Список стен для обработки
    walls = []

    def add_walls(x, y):
        """Добавляет соседние стены клетки в список"""
        if x > 1:
            walls.append((x - 1, y, x - 2, y))
        if x < width - 2:
            walls.append((x + 1, y, x + 2, y))
        if y > 1:
            walls.append((x, y - 1, x, y - 2))
        if y < height - 2:
            walls.append((x, y + 1, x, y + 2))

    add_walls(start_x, start_y)

    # Основной цикл алгоритма Прима
    while walls:
        # Выбираем случайную стену
        wall_x, wall_y, next_x, next_y = random.choice(walls)
        walls.remove((wall_x, wall_y, next_x, next_y))

        # Если клетка за стеной ещё не посещена
        if matrix[next_y][next_x] == 1:
            # Пробиваем стену и клетку
            matrix[wall_y][wall_x] = 0
            matrix[next_y][next_x] = 0
            # Добавляем новые стены
            add_walls(next_x, next_y)

    # ЭТАП 2: Создание циклов (удаление дополнительных стен)
    if cycle_percent > 0:
        # Собираем все внутренние стены
        inner_walls = []
        for y in range(2, height - 2):
            for x in range(2, width - 2):
                if matrix[y][x] == 1:
                    # Проверяем что это стена между двумя путями
                    # (горизонтальная или вертикальная)
                    if (matrix[y][x - 1] == 0 and matrix[y][x + 1] == 0) or \
                            (matrix[y - 1][x] == 0 and matrix[y + 1][x] == 0):
                        inner_walls.append((x, y))

        # Вычисляем количество стен для удаления
        walls_to_remove = int(len(inner_walls) * cycle_percent / 100)

        # Случайно удаляем стены
        if inner_walls:
            walls_to_delete = random.sample(inner_walls,
                                            min(walls_to_remove, len(inner_walls)))
            for x, y in walls_to_delete:
                matrix[y][x] = 0

    return matrix


def set_pacman_position(matrix):
    rand = random.random()
    if rand <=0.25 and matrix[1][1] == 0:
        return 1, 1
    elif 0.25 < rand <= 0.5 and matrix[1][len(matrix[0])-2] == 0:
        return 1, len(matrix[0]) - 2
    elif 0.5 < rand <= 0.75 and matrix[len(matrix)-2][1] == 0:
        return len(matrix) - 2,1
    else:
        return len(matrix) - 2, len(matrix[0]) - 2

def set_ghost_cage(matrix):
    start_row = (len(matrix) - 2) // 2
    start_col = (len(matrix[0]) - 3) // 2
    for i in range(start_row, start_row + 2):
        for j in range(start_col, start_col + 3):
            matrix[i][j] = 0
            if (i, j)!=(start_row, start_col+2):
                yield i,j

def coords_to_pixels(cord, TILE_SIZE = 32):
    """превращение координат из матрицы в пиксельное значение"""
    return int(cord*TILE_SIZE)

def debug_matrix(matrix):
    for row in matrix:
        for col in row:
            if col == 0:
                print("⬜", end=' ')
            if col == 1:
                print("⬛", end=" ")
            if col == 2:
                print("❤️", end=" ")
            if col == 3:
                print("😒", end=" ")
        print()

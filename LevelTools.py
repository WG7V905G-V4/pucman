import random
from EnvironmentVariables import *

def generate_maze_with_cycles(width, height, cycle_percent=15):
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    matrix = [[1 for _ in range(width)] for _ in range(height)]
    start_x, start_y = 1, 1
    matrix[start_y][start_x] = 0
    walls = []
    def add_walls(x, y):
        if x > 1:
            walls.append((x - 1, y, x - 2, y))
        if x < width - 2:
            walls.append((x + 1, y, x + 2, y))
        if y > 1:
            walls.append((x, y - 1, x, y - 2))
        if y < height - 2:
            walls.append((x, y + 1, x, y + 2))
    add_walls(start_x, start_y)
    while walls:
        wall_x, wall_y, next_x, next_y = random.choice(walls)
        walls.remove((wall_x, wall_y, next_x, next_y))
        if matrix[next_y][next_x] == 1:
            matrix[wall_y][wall_x] = 0
            matrix[next_y][next_x] = 0
            add_walls(next_x, next_y)
    if cycle_percent > 0:
        inner_walls = []
        for y in range(2, height - 2):
            for x in range(2, width - 2):
                if matrix[y][x] == 1:
                    if (matrix[y][x - 1] == 0 and matrix[y][x + 1] == 0) or \
                            (matrix[y - 1][x] == 0 and matrix[y + 1][x] == 0):
                        inner_walls.append((x, y))
        walls_to_remove = int(len(inner_walls) * cycle_percent / 100)
        if inner_walls:
            walls_to_delete = random.sample(inner_walls,
                                            min(walls_to_remove, len(inner_walls)))
            for x, y in walls_to_delete:
                matrix[y][x] = 0
    return matrix


def set_pacman_position(matrix):
    rand = random.random()
    if rand <=0.25 and matrix[1][1] == 0:
        matrix[1][1] = 3
    elif 0.25 < rand <= 0.5 and matrix[1][len(matrix[0])-2] == 0:
        matrix[1][ len(matrix[0]) - 2] = 3
    elif 0.5 < rand <= 0.75 and matrix[len(matrix)-2][1] == 0:
        matrix[len(matrix) - 2][1] = 3
    else:
        matrix[len(matrix) - 2][ len(matrix[0]) - 2] = 3

def set_ghost_cage(matrix):
    x,y  = len(matrix)//2, len(matrix)//2
    matrix[y][x] = 2

def coords_to_pixels(cords):
    return tuple([cord*TILE_SIZE+TILE_SIZE//2 for cord in cords])


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

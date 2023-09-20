import pygame as pg
import random
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#  Ajustes del Juego
WIDTH = 800    #  16 * 64 o 32 * 32 o 64 * 16
HEIGHT = 800    #  16 * 48 o 32 * 24 o 64 * 12
SCREENSIZE = (WIDTH, HEIGHT)
MARGIN = 5
FPS = 60
TITLE = "Mapa Test"

BGCOLOR = pg.image.load("resources/sprites/background.png")
BGCOLOR = pg.transform.scale(BGCOLOR, SCREENSIZE)

BGEND = pg.image.load("resources/sprites/empty.png")
BGEND = pg.transform.scale(BGCOLOR, SCREENSIZE)

#  Tamaño de los espacios y de las columnas y renglones.
TITLESIZE = 15
GRIDWIDTH = WIDTH / TITLESIZE
GRIDHEIGHT = HEIGHT / TITLESIZE

mapDraw = []

rows = 10
columns = 10
max_obstacles = 25
min_distance = 8

levelMap = [[0 for _ in range(columns)] for _ in range(rows)]


def distance(position1, position2):
    return math.sqrt((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2)


player_position = (random.randint(0, rows - 1), random.randint(0, columns - 1))

while True:
    enemy_position = (random.randint(0, rows - 1), random.randint(0, columns - 1))
    if distance(player_position, enemy_position) >= min_distance:
        break

levelMap[player_position[0]][player_position[1]] = 1
levelMap[enemy_position[0]][enemy_position[1]] = 2

for _ in range(max_obstacles):
    while True:
        row = random.randint(0, rows - 1)
        column = random.randint(0, columns - 1)
        if levelMap[row][column] == 0:
            levelMap[row][column] = 3
            break
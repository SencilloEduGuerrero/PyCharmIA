import pygame as pg
import random
import math

# Colores
BLACK = (0, 0, 0)

#  Ajustes del Juego
WIDTH = 800  # 16 * 64 o 32 * 32 o 64 * 16
HEIGHT = 800  # 16 * 48 o 32 * 24 o 64 * 12
SCREENSIZE = (WIDTH, HEIGHT)
MARGIN = 5

# Fondos
# BGCOLOR = Fondo de diseño
BGCOLOR = pg.image.load("resources/sprites/background.png")
BGCOLOR = pg.transform.scale(BGCOLOR, SCREENSIZE)

BGCOLOR1 = pg.image.load("resources/sprites/background1.png")
BGCOLOR1 = pg.transform.scale(BGCOLOR1, SCREENSIZE)

BGCOLOR2 = pg.image.load("resources/sprites/background2.png")
BGCOLOR2 = pg.transform.scale(BGCOLOR2, SCREENSIZE)

BGCOLOR3 = pg.image.load("resources/sprites/background3.png")
BGCOLOR3 = pg.transform.scale(BGCOLOR3, SCREENSIZE)

BGCOLOR4 = pg.image.load("resources/sprites/background4.png")
BGCOLOR4 = pg.transform.scale(BGCOLOR4, SCREENSIZE)

BGCOLOR5 = pg.image.load("resources/sprites/background5.png")
BGCOLOR5 = pg.transform.scale(BGCOLOR5, SCREENSIZE)

BGCOLOR6 = pg.image.load("resources/sprites/background6.png")
BGCOLOR6 = pg.transform.scale(BGCOLOR6, SCREENSIZE)

BGCOLOR7 = pg.image.load("resources/sprites/background7.png")
BGCOLOR7 = pg.transform.scale(BGCOLOR7, SCREENSIZE)

BGCOLOR8 = pg.image.load("resources/sprites/background8.png")
BGCOLOR8 = pg.transform.scale(BGCOLOR8, SCREENSIZE)

BGCOLOR9 = pg.image.load("resources/sprites/background9.png")
BGCOLOR9 = pg.transform.scale(BGCOLOR9, SCREENSIZE)

# BGPAUSE = Fondo en caso de Pausar
BGPAUSE = pg.image.load("resources/sprites/pause.png")
BGPAUSE = pg.transform.scale(BGPAUSE, SCREENSIZE)

#  Tamaño de los espacios y de las columnas y renglones.
TITLESIZE = 15
GRIDWIDTH = WIDTH / TITLESIZE
GRIDHEIGHT = HEIGHT / TITLESIZE

# Creación del Mapa
mapDraw = []

# Variables
rows = 10
columns = 10
max_obstacles = 35
min_distance = 4
max_distance = 8
max_limit_4 = 6
max_limit_5 = 3
count_4 = 0
count_5 = 0

# Crea el arreglo del mapa 10x10
levelMap = [[0 for _ in range(columns)] for _ in range(rows)]


# Método para validacion de distancia entre la meta y el jugador
def distance(position1, position2):
    return math.sqrt((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2)


# Crea la posición aleatoria de
goal_position = (random.randint(0, rows - 1), random.randint(0, columns - 1))

# Validacion para dar un rango maximo/minimo a la meta y a Kirby
while True:
    kirby_position = (random.randint(0, rows - 1), random.randint(0, columns - 1))
    if distance(goal_position, kirby_position) >= max_distance:
        break
    elif distance(goal_position, kirby_position) >= min_distance:
        break

# Asigna la posicion y valores
levelMap[goal_position[0]][goal_position[1]] = 1
levelMap[kirby_position[0]][kirby_position[1]] = 2

# Establecemos un limite de ostaculos y contador para validar.
for _ in range(max_obstacles):
    while True:
        row = random.randint(0, rows - 1)
        column = random.randint(0, columns - 1)
        if count_4 < max_limit_4 and levelMap[row][column] == 0:
            levelMap[row][column] = 4
            count_4 += 1
            break
        if count_5 < max_limit_5 and levelMap[row][column] == 0:
            levelMap[row][column] = 5
            count_5 += 1
            break
        elif levelMap[row][column] == 0:
            levelMap[row][column] = 3
            break
#  Colores
import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#  Ajustes del Juego
WIDTH = 1024    #  16 * 64 o 32 * 32 o 64 * 16
HEIGHT = 1024    #  16 * 48 o 32 * 24 o 64 * 12
SCREENSIZE = (WIDTH, HEIGHT)
FPS = 60
TITLE = "Mapa Test"
BGCOLOR = pg.image.load("resources/sprites/background.png")
BGCOLOR = pg.transform.scale(BGCOLOR, SCREENSIZE)

LOADSCREEN = pg.image.load("resources/sprites/ScreenSpriteA.png")
LOADSCREEN = pg.transform.scale(LOADSCREEN, SCREENSIZE)

max_enemies = 10
enemy_count = 0

#  Tamaño de los espacios y de las columnas y renglones.
TITLESIZE = 64
GRIDWIDTH = WIDTH / TITLESIZE
GRIDHEIGHT = HEIGHT / TITLESIZE
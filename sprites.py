import random
import pygame as pg
from settings import *


#  Se crea la clase del jugador, donde se asigna su sprite, en donde estará.
#  tamaño, su dibujo que es un rectangulo y sus posiciones.
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("resources/sprites/kirbySpriteD.png")
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

#  Metodo de movimiento, que toma su posición y utiliza auxiliares.
#  si detecta el otro metodo de colisión, conserva su posición.
    def move(self, dx = 0, dy = 0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

#  Método de colisión con paredes, donde toma la pared y crea una
#  validación donde se compara si las coordenas coinciden para dar colisión.
    def collide_with_walls(self, dx = 0, dy = 0):
        if ( self.x == 0 and  dx < 0 )or( self.y == 0 and dy < 0):
         return True
        if (self.x == 15 and dx > 0) or (self.y == 15 and dy > 0):
            return True
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

#  Método de actualizar y sincronizar los rectangulos con las posiciones o coordenadas.
    def update(self):
        self.rect.x = self.x * TITLESIZE
        self.rect.y = self.y * TITLESIZE

#  Clase de pared, donde se crea su grupo, dibuja su sprite, se coloca, toma el tamaño
#  toma sus posiciones y respeta las coordenadas.
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TITLESIZE, TITLESIZE))
        self.image = pg.image.load("resources/sprites/wallSprite.png")
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TITLESIZE
        self.rect.y = y * TITLESIZE

class Goal(pg.sprite.Sprite): #Ajustar clase a clase Poderes y hacerle modificaciones
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("resources/sprites/goal.png")
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TITLESIZE
        self.rect.y = self.y * TITLESIZE

# Aun no esta terminado u _ u
class Food(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("resources/sprites/food.png")
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        rand = random.randrange(0, 2)

        match rand:
            case 0:
                self.image = pg.image.load("resources/sprites/fireEnemyD.png")
            case 1:
                self.image = pg.image.load("resources/sprites/iceEnemyD.png")
            #case 2:
            #    self.image = pg.image.load("resources/sprites/thunderEnemyD.png")
            #case 3:
            #    self.image = pg.image.load("resources/sprites/windEnemyD.png")
            #case 4:
            #    self.image = pg.image.load("resources/sprites/swordEnemyD.png")

        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TITLESIZE
        self.rect.y = self.y * TITLESIZE
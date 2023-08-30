import random

from settings import *
from sprites import *
import pygame as pg
import sys

#  Clase Main conocida como 'Game'
#  en esta clase se define la pantalla con su tamaño, display.
#  se crea un reloj interno para los FPS.
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100) #  Es el delay que se pone si se mantiene presionado un botón.
        self.load_data()

#  Método de cargar información pero aún no tiene nada.
    def load_data(self):
        pass

#  En 'new' toma los sprites dibujados, primero toma al jugador
#  toma sus atributos y lo dibuja en la posición (x = 1, y = 7)
#  walls sería la clase de paredes, donde se dibujan creando fors,
#  en lugar de ir dibujando una pared por una.
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 1, 1)
        self.goals = []
        for _ in range(random.randrange(4,12)):
            goal = Goal(self, random.randrange(0,14), random.randrange(0, 14))
            self.goals.append(goal)
        #self.goal = Goal(self, random.randrange(0,14), random.randrange(0, 14))
        self.walls = pg.sprite.Group()
        for x in range(0, 16):
            for y in range(0, 16):
                rand = random.randrange(0, 10)
                if rand > 7:
                    if not (x == self.player.x and y == self.player.y) and not any(goal.x == x and goal.y == y for goal in self.goals):
                        Wall(self, x, y)



#  run es lo que ejecuta o permite crear el tiempo y así
#  poder tener un movimiento o animación, donde traza
#  los eventos, los actualiza y los dibuja para que sea
#  sincronizado.
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

#  Método para cerrar el proyecto y salir del sistema.
    def quit(self):
        pg.quit()
        sys.exit()

#  Actualiza los sprites para que si hay algún cambio se note.
    def update(self):
        self.all_sprites.update()

#  Dibuja lo que serían las columnas y filas tomando en cuenta el tamaño de la pantalla.
    def draw_grid(self):
        for x in range(0, WIDTH, TITLESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TITLESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

#  Dibuja el fondo, las columnas y filas, y también los sprites que se dibujarán.
#  display.flip actualiza y verifica, se ubica al final.
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

#  Los eventos en resumida cuenta son los que al recibir una indicación realiza una
#  acción, como el botón para cerrar o moverse.
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            #  Para la IA se desactivaría de aquí...
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.new()
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx = -1)
                    self.player.image = pg.image.load("resources/sprites/kirbySpriteL.png")
                    self.player.image = pg.transform.scale(self.player.image, (64, 64))
                if event.key == pg.K_RIGHT:
                    self.player.move(dx = 1)
                    self.player.image = pg.image.load("resources/sprites/kirbySpriteR.png")
                    self.player.image = pg.transform.scale(self.player.image, (64, 64))
                if event.key == pg.K_UP:
                    self.player.move(dy = -1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy = 1)
                for goal in self.goals:
                    if self.player.x == goal.x and self.player.y == goal.y:
                        self.player.image = pg.image.load("resources/sprites/victoryKirby.png")
                        self.player.image = pg.transform.scale(self.player.image, (64, 64))
                        goal.kill()  #Alternativa a eliminar una imagen
            #  hasta aqui...

#  Pantalla de inicio, aun no tiene nada.
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

#  Es lo que ejecuta y abre la pantalla del juego, sin esto no se crea la ventana.
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
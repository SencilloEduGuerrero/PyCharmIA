from settings import *


# Class Meta donde asignamos su posición y actualización
class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.x = self.x * TITLESIZE
        self.y = self.y * TITLESIZE


# Class Kirby donde asignamos su posición, estado, vida
class Kirby:
    def __init__(self, x, y, max_health):
        self.x = x
        self.y = y
        self.alive = True
        self.health = 100
        self.max_health = max_health
        self.health = max_health
        self.health_bar_width = 185
        self.health_bar_height = 50
        self.health_bar_color = (255, 192, 203)
        self.health_bar_background_color = (0, 0, 0)

    # Metodo para asignar y dibujar la barra de vida del personaje
    def draw_health_bar(self, screen):
        health_percentage = max(0, self.health) / self.max_health
        bar_width = int(self.health_bar_width * health_percentage)

        health_bar_bg_rect = pg.Rect(11 * TITLESIZE, 44 * TITLESIZE, self.health_bar_width, self.health_bar_height)
        pg.draw.rect(screen, self.health_bar_background_color, health_bar_bg_rect)

        background_width = self.health_bar_width - bar_width
        health_bar_background_rect = pg.Rect(
            (11 + bar_width) * TITLESIZE, 44 * TITLESIZE, background_width, self.health_bar_height
        )
        pg.draw.rect(screen, (0, 0, 0), health_bar_background_rect)

        health_bar_rect = pg.Rect(11 * TITLESIZE, 44 * TITLESIZE, bar_width, self.health_bar_height)
        pg.draw.rect(screen, self.health_bar_color, health_bar_rect)

    # Metodo para verificar si Kirby esta vivo o no
    def status(self):
        if self.alive:
            return 'ALIVE'

        return 'DEATH'

    def update(self):
        self.x = self.x * TITLESIZE
        self.y = self.y * TITLESIZE


# Class de la HUD, donde dibuja la interfaz
class HUD:
    def __init__(self, x, y):
        self.image = pg.image.load("resources/sprites/HudFormatK.png")
        self.image = pg.transform.scale(self.image, (WIDTH, 192))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TITLESIZE
        self.rect.y = self.y * TITLESIZE


# Class Nodo
# En la class Nodo, creamos los valores de la heuristica y costos para el algoritmo estrella.
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = 0

    def __eq__(self, other):
        return self.position == other.position


# Algoritmo Estrella (A*).
def astar(maze, start, end):
    # Variables que obtienen los valores de inicio, nodos y fin.
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Funcionan como listas que agregan el camino que los nodos ya exploraron.
    open_list = []
    closed_list = []

    open_list.append(start_node)
    prev_position = None

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0

        # Encuentra el nodo con el valor más bajo en la lista del camino.
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Remueve el nodo con el valor más bajo de la lista 'open' pero lo agrega en 'close'
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Validación para verificar si el nodo actual esta en el nodo destino (para terminar el proceso).
        if current_node == end_node:
            path = []
            current = current_node

            # Reconstruye el camino para seguir buscando el punto padre (En caso de que el personaje tiene poca vida,
            # regresa a cumplir la función de obtener la meta).
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        # Generamos los nodos hijos para el movimiento.
        children = []
        for new_position, cost in [((0, -1), 1), ((0, 1), 1), ((-1, 0), 1), ((1, 0), 1)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Verifica si la nueva posición está dentro de los limites del laberinto (Para evitar que el nodo salga del
            # mapa al intentar buscar el camino).
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Verifica si la nueva posición está bloqueada por obstaculos.
            if maze[node_position[0]][node_position[1]] not in (0, 1, 4, 5, 2):
                continue

            # Creamos nuevos nodos por un movimiento válido.
            new_node = Node(current_node, node_position)
            new_node.g = current_node.g + cost
            # Actualiza el costo para llegar al nodo.
            new_node.cost = cost

            # Verifica si el nuevo node esta en la lista 'open'
            if new_node in open_list:
                existing_node = open_list[open_list.index(new_node)]
                # Si el nuevo camino al nodo es corto, actualiza los valores.
                if new_node.g < existing_node.g:
                    open_list.remove(existing_node)
                    open_list.append(new_node)
            # Verifica si el nuevo nodo esta ya en la lista 'closed'
            elif new_node in closed_list:
                existing_node = closed_list[closed_list.index(new_node)]
                # Verifica si el nuevo camino es mas corto, y lo mueve de regreso a la lista 'open'
                if new_node.g < existing_node.g:
                    closed_list.remove(existing_node)
                    open_list.append(new_node)
            else:
                children.append(new_node)

        # Calcula la heurística y costo total por cada nodo hijo.
        for child in children:
            # Validación que detecta si el camino es posible de resolver, en caso de que no
            # regresa un bool de validación.
            if end_node is not None:
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h
            else:
                errorValidation = True

        # Añade el 'children' a la lista 'open' para la exploración.
        open_list.extend(children)

        # Validación para loops atorados, si el nodo es igual al de la anterior posición regresa un None.
        if current_node.position == prev_position:
            return None

        prev_position = current_node.position
    # Si la lista 'open' esta vacía sin encontrar algún camino, regresa
    # None para evitar que el proyecto se crashee o cierre.
    return None
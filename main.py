from sprites import *
from settings import *
import time
import pygame as pg


player_position = None
player_alive = True
enemy_position = None
hud = HUD(0, 40)

for row_idx, row in enumerate(levelMap):
    for col_idx, value in enumerate(row):
        if value == 1:
            player_position = (row_idx, col_idx)
        elif value == 2:
            enemy_position = (row_idx, col_idx)

if player_position is not None:
    player = Player(player_position[0], player_position[1], 100)

if enemy_position is not None:
    enemy = Enemy(enemy_position[0], enemy_position[1])

mapDraw = levelMap

last_movement_time = pg.time.get_ticks()
movement_interval = 500

start = (enemy.x, enemy.y)
end = (player.x, player.y)

path = astar(mapDraw, start, end)

pg.init()
pg.font.init()

custom_font = pg.font.Font("resources/fonts/Pixel Emulator.otf", 25)
custom_fontH = pg.font.Font("resources/fonts/Pixel Emulator.otf", 23)
startTime = time.time()
pg.font.init()
levelText = custom_font.render('Level Test', True, (255, 255, 255))
healthText = custom_fontH.render(str(player.health) + '/100', True, (255, 255, 255))
enemyText = custom_font.render('Enemies: ' + str(enemy.status()), True, (255, 255, 255))
levelTextR = levelText.get_rect()
healthTextR = healthText.get_rect()
enemyTextR = enemyText.get_rect()
levelTextR.center = (695, 45)
healthTextR.center = (260, 680)
enemyTextR.center = (585, 725)
timeText = custom_font.render("Time: " + str(0), True, (0, 0, 0))
timeTextR = timeText.get_rect()
timeTextR.center = (520, 670)


def algorith():
    if player.health <= 30:
        nearest_health_space = find_nearest_health_space((enemy.x, enemy.y), mapDraw)

        if nearest_health_space:
            enemy_path = astar(mapDraw, (enemy.x, enemy.y), nearest_health_space)

            if enemy_path:
                next_position = enemy_path[1]
                tile_value = mapDraw[next_position[0]][next_position[1]]
                if tile_value == 5:
                    player.health += 10
                mapDraw[enemy.x][enemy.y] = 0
                enemy.x, enemy.y = next_position
                mapDraw[enemy.x][enemy.y] = 2
                return

    maze = astar(mapDraw, (enemy.x, enemy.y), (player.x, player.y))

    if maze:
        mapDraw[enemy.x][enemy.y] = 0

        if maze[1][0] == player.x and maze[1][1] == player.y:
            mapDraw[maze[1][0]][maze[1][1]] = 0
        elif mapDraw[maze[1][0]][maze[1][1]] == 4:
            mapDraw[maze[1][0]][maze[1][1]] = 0
            player.health -= 10
        else:
            enemy.x = maze[1][0]
            enemy.y = maze[1][1]
            mapDraw[enemy.x][enemy.y] = 2


def find_nearest_mine(start_position):
    mines = [(row, col) for row in range(len(mapDraw)) for col in range(len(mapDraw[0])) if mapDraw[row][col] == 5]

    if not mines:
        return None

    nearest_mine = min(mines, key=lambda pos: abs(pos[0] - start_position[0]) + abs(pos[1] - start_position[1]))
    return nearest_mine


def find_nearest_health_space(start_position, mapDraw):
    open_list = []
    closed_set = set()

    open_list.append(Node(None, start_position))

    while open_list:
        current_node = open_list.pop(0)

        if mapDraw[current_node.position[0]][current_node.position[1]] == 5:  # Health space
            return current_node.position

        closed_set.add(current_node.position)

        adjacent_positions = [(current_node.position[0] + dy, current_node.position[1] + dx)
                              for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]]

        for neighbor in adjacent_positions:
            if neighbor[0] < 0 or neighbor[0] >= len(mapDraw) or \
               neighbor[1] < 0 or neighbor[1] >= len(mapDraw[0]) or \
               mapDraw[neighbor[0]][neighbor[1]] == 3 or \
               neighbor in closed_set:
                continue

            new_node = Node(current_node, neighbor)
            open_list.append(new_node)

    return None


def drawUI():
    endTime = time.time()
    timeText = custom_font.render("Time: " + str(int(endTime - startTime)), True, (0, 0, 0))
    healthText = custom_font.render(str(player.health) + "/100", True, (255, 0, 0))
    enemyText = custom_font.render("Enemy: " + str(enemy.status()), True, (0, 0, 0))
    screen.blit(timeText, timeTextR)
    screen.blit(levelText, levelTextR)
    screen.blit(enemyText, enemyTextR)
    screen.blit(healthText, healthTextR)


def update_screen():
    if player.health <= 0:
        player.health = 0
        player.alive = False
        screen.fill(BLACK)
    if player.health >= 100:
        player.health = 100


screen = pg.display.set_mode(SCREENSIZE)
pg.display.set_caption("Test Game")

done = False
paused = False
clock = pg.time.Clock()

while not done:
    for event in pg.event.get():
        keys = pg.key.get_pressed()
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True

    screen.blit(BGCOLOR, (0, 0))

    if not paused:
        current_time = pg.time.get_ticks()
        if current_time - last_movement_time >= movement_interval:
            algorith()
            last_movement_time = current_time

        update_screen()

        hud.update()
        player.draw_health_bar(screen)

        screen.blit(hud.image, (hud.rect.x, hud.rect.y))

    for row in range(10):
        for column in range(10):
            texture = None
            color = pg.Color(255, 255, 255, 25)

            if mapDraw[row][column] == 1:
                color = pg.Color(0, 255, 0, 255)
            elif mapDraw[row][column] == 2:
                color = pg.Color(255, 0, 0, 255)
            elif mapDraw[row][column] == 3:
                texture = pg.image.load("resources/sprites/wallSprite.png").convert_alpha()
                texture = pg.transform.scale(texture, (52, 52))
            elif mapDraw[row][column] == 4:
                color = pg.Color(255, 255, 0, 255)
            elif mapDraw[row][column] == 5:
                color = pg.Color(255, 255, 255, 255)

            if texture is not None:
                screen.blit(texture, ((MARGIN + GRIDWIDTH) * column + MARGIN, (MARGIN + GRIDHEIGHT) * row + MARGIN))

            rect_surface = pg.Surface((GRIDWIDTH, GRIDHEIGHT), pg.SRCALPHA)
            pg.draw.rect(rect_surface, color, (0, 0, GRIDWIDTH, GRIDHEIGHT))

            screen.blit(rect_surface, ((MARGIN + GRIDWIDTH) * column + MARGIN,
                                       (MARGIN + GRIDHEIGHT) * row + MARGIN))

    drawUI()

    clock.tick(30)
    pg.display.flip()

pg.quit()
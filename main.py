from sprites import *
from settings import *
import time
import pygame as pg

player_position = None
player_alive = True
enemy_position = None
hud = HUD(0, 40)
algorithm_active = True

for row_idx, row in enumerate(levelMap):
    for col_idx, value in enumerate(row):
        if value == 1:
            player_position = (row_idx, col_idx)
        elif value == 2:
            enemy_position = (row_idx, col_idx)

player = Player(player_position[0], player_position[1], 100) if player_position is not None else None
enemy = Enemy(enemy_position[0], enemy_position[1]) if enemy_position is not None else None

mapDraw = levelMap


def has_dead_ends(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 0:
                neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                passages = sum(
                    1 for r, c in neighbors if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] == 0)
                if passages <= 1:
                    return True
    return False


last_movement_time = pg.time.get_ticks()
movement_interval = 500

start = (enemy.x, enemy.y)
end = (player.x, player.y)

if has_dead_ends(mapDraw):
    print("Maze has dead-ends and may be unsolvable.")
else:
    path = astar(mapDraw, start, end, 5)

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
    if not algorithm_active:
        return

    if player.health <= 40:
        nearest_health_space = find_nearest_health_space((enemy.x, enemy.y), mapDraw)

        if nearest_health_space:
            enemy_path = astar(mapDraw, (enemy.x, enemy.y), nearest_health_space, 5)

            if enemy_path:
                next_position = enemy_path[1]
                tile_value = mapDraw[next_position[0]][next_position[1]]
                if tile_value == 5:
                    player.health += 20
                mapDraw[enemy.x][enemy.y] = 0
                enemy.x, enemy.y = next_position
                mapDraw[enemy.x][enemy.y] = 2
                return

    maze = astar(mapDraw, (enemy.x, enemy.y), (player.x, player.y), 5)

    if maze:
        mapDraw[enemy.x][enemy.y] = 0

        if maze[1][0] == player.x and maze[1][1] == player.y:
            mapDraw[maze[1][0]][maze[1][1]] = 0
        elif mapDraw[maze[1][0]][maze[1][1]] == 4:
            mapDraw[maze[1][0]][maze[1][1]] = 0
            player.health -= 20
        elif mapDraw[maze[1][0]][maze[1][1]] == 5:
            mapDraw[maze[1][0]][maze[1][1]] = 0
            player.health += 20
        else:
            enemy.x = maze[1][0]
            enemy.y = maze[1][1]
            mapDraw[enemy.x][enemy.y] = 2


def find_nearest_health_space(start_position, mapDraw):
    open_list = []
    closed_set = set()

    open_list.append(Node(None, start_position))

    while open_list:
        current_node = open_list.pop(0)

        if mapDraw[current_node.position[0]][current_node.position[1]] == 5:
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


def reset_game():
    global algorithm_active
    global player
    global enemy

    algorithm_active = True

    player_position = (random.randint(0, rows - 1), random.randint(0, columns - 1))
    enemy_position = (random.randint(0, rows - 1), random.randint(0, columns - 1))

    player = Player(player_position[0], player_position[1], 100)
    enemy = Enemy(enemy_position[0], enemy_position[1])


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
            elif event.key == pg.K_r:
                if not algorithm_active:
                    reset_game()
            elif event.key == pg.K_s:
                algorithm_active = not algorithm_active

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

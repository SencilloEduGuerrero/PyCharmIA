from sprites import *
from settings import *
import time
import pygame as pg
import random

optimal_path = []

goal_position = None
kirby_position = None
hud = HUD(0, 40)
algorithm_active = True
aCount_4 = 0
aCount_5 = 0
move_count = 0
auxTime = 0
is_imposible = False
finished = False
values_on = False
error_validation = False

randomBG = (random.randint(0, 9))

for row_idx, row in enumerate(levelMap):
    for col_idx, value in enumerate(row):
        if value == 1:
            goal_position = (row_idx, col_idx)
        elif value == 2:
            kirby_position = (row_idx, col_idx)

goal = Goal(goal_position[0], goal_position[1]) if goal_position is not None else None
kirby = Kirby(kirby_position[0], kirby_position[1], 100) if kirby_position is not None else None

mapDraw = levelMap

last_movement_time = pg.time.get_ticks()
movement_interval = 500

start = (kirby.x, kirby.y)
end = (goal.x, goal.y)

pg.init()
pg.font.init()

custom_fontP = pg.font.Font("resources/fonts/Pixel Emulator.otf", 70)
custom_fontD = pg.font.Font("resources/fonts/Pixel Emulator.otf", 30)
custom_font = pg.font.Font("resources/fonts/Pixel Emulator.otf", 25)
custom_fontH = pg.font.Font("resources/fonts/Pixel Emulator.otf", 23)
custom_fontM = pg.font.Font("resources/fonts/Pixel Emulator.otf", 15)
startTime = time.time()
pg.font.init()

healthText = custom_fontH.render(str(kirby.health) + '/100', True, (255, 255, 255))
statusText = custom_font.render('Status: ' + str(kirby.status()), True, (255, 255, 255))
damageText = custom_font.render('Danger: ' + str(int(count_4 - aCount_4)), True, (255, 255, 255))
healText = custom_font.render('Heal: ' + str(int(count_5 - aCount_5)), True, (255, 255, 255))
moveText = custom_fontM.render('Movements: ' + str(int(move_count)), True, (255, 255, 255))
helpText = custom_fontM.render('Press "S" to Pause', True, (255, 255, 255))
pathText = custom_fontM.render('Press "Q" to Path', True, (255, 255, 255))
closeText = custom_fontM.render('Press "ESC" to Quit', True, (255, 255, 255))

pauseText = custom_fontP.render('PAUSE', True, (0, 0, 255))
descText = custom_fontD.render('Get the Goal!', True, (0, 0, 0))
descText2 = custom_fontD.render('Beware with the Enemies!', True, (0, 0, 0))
descText3 = custom_fontD.render('Eat food to heal!', True, (0, 0, 0))
resumeText = custom_font.render('Press "S" to Resume', True, (255, 255, 255))
resetText = custom_font.render('Press "R" to Reset Game', True, (255, 255, 255))
quitText = custom_font.render('Press "ESC" to Quit', True, (255, 255, 255))

gameOverText = custom_fontP.render('GAMEOVER', True, (255, 255, 255))
ErrorTextA = custom_font.render('Error! Something Went Wrong', True, (255, 255, 255))
ErrorTextB = custom_font.render('Please Restart the Game', True, (255, 255, 255))

healthTextR = healthText.get_rect()
statusTextR = statusText.get_rect()
damageTextR = damageText.get_rect()
healTextR = healthText.get_rect()
moveTextR = moveText.get_rect()
helpTextR = helpText.get_rect()
pathTextR = pathText.get_rect()
closeTextR = closeText.get_rect()

descTextR = descText.get_rect()
descTextR2 = descText2.get_rect()
descTextR3 = descText3.get_rect()
pauseTextR = pauseText.get_rect()
resumeTextR = resumeText.get_rect()
resetTextR = resetText.get_rect()
quitTextR = quitText.get_rect()

gameOverTextR = gameOverText.get_rect()
ErrorTextAR = ErrorTextA.get_rect()
ErrorTextBR = ErrorTextB.get_rect()

healthTextR.center = (260, 680)
statusTextR.center = (575, 725)
damageTextR.center = (695, 95)
healTextR.center = (695, 125)
moveTextR.center = (650, 155)
helpTextR.center = (690, 215)
pathTextR.center = (690, 235)
closeTextR.center = (685, 255)

descTextR.center = (290, 230)
descTextR2.center = (410, 300)
descTextR3.center = (335, 370)
pauseTextR.center = (480, 90)
resumeTextR.center = (315, 570)
resetTextR.center = (355, 650)
quitTextR.center = (315, 730)

gameOverTextR.center = (WIDTH/2, HEIGHT/3)
ErrorTextAR.center = (WIDTH/2, HEIGHT/3 - 20)
ErrorTextBR.center = (WIDTH/2, HEIGHT/3 + 20)

timeText = custom_font.render("Time: " + str(0), True, (0, 0, 0))
timeTextR = timeText.get_rect()
timeTextR.center = (520, 670)


def algorith():
    global aCount_4, aCount_5, move_count, is_imposible, finished
    objectionMovement = False

    if kirby.health == 0:
        return

    if not algorithm_active:
        draw_pause_screen()
        return

    prev_kirby_position = (kirby.x, kirby.y)
    prev_kirby_direction = None

    if kirby.health <= 40:
        nearest_health_space = find_nearest_health_space((kirby.x, kirby.y), mapDraw)

        if nearest_health_space:
            kirby_path = astar(mapDraw, (kirby.x, kirby.y), nearest_health_space, 5)

            if kirby_path:
                next_position = kirby_path[1]
                tile_value = mapDraw[next_position[0]][next_position[1]]
                if tile_value == 5:
                    aCount_5 += 1
                    kirby.health += 20
                if tile_value == 4:
                    aCount_4 += 1
                    kirby.health -= 20
                if tile_value == 1:
                    mapDraw[goal.x][goal.y] = 0
                    finished
                    return
                mapDraw[kirby.x][kirby.y] = 0
                kirby.x, kirby.y = next_position
                mapDraw[kirby.x][kirby.y] = 2
                return

    if (kirby.x, kirby.y) != (goal.x, goal.y) and algorithm_active:
        maze = astar(mapDraw, (kirby.x, kirby.y), (goal.x, goal.y), 5)

        if maze:
            mapDraw[kirby.x][kirby.y] = 0

            if maze[1][0] == goal.x and maze[1][1] == goal.y:
                mapDraw[maze[1][0]][maze[1][1]] = 0
                objectionMovement = True
                finished = True
            elif mapDraw[maze[1][0]][maze[1][1]] == 4:
                mapDraw[maze[1][0]][maze[1][1]] = 0
                kirby.health -= 20
                aCount_4 += 1
                objectionMovement = True
            elif mapDraw[maze[1][0]][maze[1][1]] == 5:
                mapDraw[maze[1][0]][maze[1][1]] = 0
                kirby.health += 20
                aCount_5 += 1
                objectionMovement = True
            else:
                kirby.x = maze[1][0]
                kirby.y = maze[1][1]
                mapDraw[kirby.x][kirby.y] = 2

                if (kirby.x, kirby.y) == prev_kirby_position and (kirby.x, kirby.y) != prev_kirby_direction:
                    prev_kirby_direction = (kirby.x, kirby.y)
                else:
                    prev_kirby_direction = None

                if move_count < 100 and prev_kirby_direction is None:
                    move_count += 1

    if (kirby.x, kirby.y) == prev_kirby_position and not objectionMovement:
        is_imposible = True
        return


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


def draw_pause_screen():
    screen.blit(BGPAUSE, (0, 0))

    descText = custom_fontD.render('Get the Goal!', True, (0, 0, 0))
    descText2 = custom_fontD.render('Beware with the Enemies!', True, (0, 0, 0))
    descText3 = custom_fontD.render('Eat food to heal!', True, (0, 0, 0))
    pauseText = custom_fontP.render('PAUSE', True, (50, 50, 220))
    resumeText = custom_font.render('Press "S" to Resume', True, (255, 255, 255))
    resetText = custom_font.render('Press "R" to Reset', True, (255, 255, 255))
    quitText = custom_font.render('Press "ESC" to Quit', True, (255, 255, 255))

    screen.blit(pauseText, pauseTextR)
    screen.blit(resumeText, resumeTextR)
    screen.blit(resetText, resetTextR)
    screen.blit(quitText, quitTextR)
    screen.blit(descText, descTextR)
    screen.blit(descText2, descTextR2)
    screen.blit(descText3, descTextR3)


def reset_game():
    global algorithm_active
    global goal
    global kirby
    global mapDraw
    global levelMap

    algorithm_active = True

    rows = 10
    columns = 10

    levelMap = [[0 for _ in range(columns)] for _ in range(rows)]

    max_obstacles = 35
    min_distance = 4
    max_distance = 8
    max_limit_4 = 6
    max_limit_5 = 3
    count_4 = 0
    count_5 = 0

    goal_position = (random.randint(0, rows - 1), random.randint(0, columns - 1))

    while True:
        kirby_position = (random.randint(0, rows - 1), random.randint(0, columns - 1))
        if distance(goal_position, kirby_position) >= max_distance:
            break
        elif distance(goal_position, kirby_position) >= min_distance:
            break

    levelMap[goal_position[0]][goal_position[1]] = 1
    levelMap[kirby_position[0]][kirby_position[1]] = 2

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

    mapDraw = levelMap
    goal = Goal(goal_position[0], goal_position[1])
    kirby = Kirby(kirby_position[0], kirby_position[1], 100)


def drawUI():
    endTime = time.time()
    auxTime = endTime - startTime
    colorPath = pg.Color(0, 255, 0, 50)

    if auxTime > 100:
        auxTime = 99

    timeText = custom_font.render("Time: " + str(int(auxTime)), True, (0, 0, 0))
    healthText = custom_fontH.render(str(kirby.health) + "/100", True, (255, 0, 0))
    statusText = custom_font.render("Status: " + str(kirby.status()), True, (0, 0, 0))
    damageText = custom_font.render('Danger: ' + str(int(count_4 - aCount_4)), True, (255, 255, 255))
    healText = custom_font.render('Heal: ' + str(int(count_5 - aCount_5)), True, (255, 255, 255))
    moveText = custom_fontH.render('Movements: ' + str(int(move_count)), True, (255, 255, 255))
    helpText = custom_fontM.render('Press "S" to Pause', True, (255, 255, 255))
    pathText = custom_fontM.render('Press "Q" to Path', True, (255, 255, 255))
    closeText = custom_fontM.render('Press "ESC" to Close', True, (255, 255, 255))

    screen.blit(timeText, timeTextR)
    screen.blit(statusText, statusTextR)
    screen.blit(healthText, healthTextR)
    screen.blit(damageText, damageTextR)
    screen.blit(healText, healTextR)
    screen.blit(moveText, moveTextR)
    screen.blit(helpText, helpTextR)
    screen.blit(pathText, pathTextR)
    screen.blit(closeText, closeTextR)

    if not values_on:
        if kirby.health == 0 or is_imposible:
            pg.draw.rect(screen, BLACK, pg.Rect(170, 200, 450, 150))
            gameOverText = custom_fontP.render('GAMEOVER', True, (255, 255, 255))
            screen.blit(gameOverText, gameOverTextR)

        if finished:
            pg.draw.rect(screen, BLACK, pg.Rect(170, 200, 490, 150))
            gameOverText = custom_fontP.render('FINISHED!', True, (255, 255, 255))
            screen.blit(gameOverText, gameOverTextR)

    if error_validation:
        pg.draw.rect(screen, BLACK, pg.Rect(50, 200, 700, 150))
        ErrorTextA = custom_font.render('Error: Something Went Wrong', True, (255, 255, 255))
        ErrorTextB = custom_font.render('Please Restart the Game', True, (255, 255, 255))
        screen.blit(ErrorTextA, ErrorTextAR)
        screen.blit(ErrorTextB, ErrorTextBR)

    if values_on:
        cell_width = 58
        cell_height = 58

        for row in range(len(mapDraw)):
            for col in range(len(mapDraw[row])):
                cell_value = mapDraw[row][col]
                cost = 0

                if cell_value == 0:
                    cost = 1

                if cost > 0:
                    text = custom_fontD.render(str(cost), True, (0, 0, 0))
                    text_rect = text.get_rect(
                        center=(col * cell_width + cell_width // 2, row * cell_height + cell_height // 2))
                    screen.blit(text, text_rect)

        agent_row, agent_col = kirby_position
        mapDraw[agent_row][agent_col] = 0

        start = (kirby.x, kirby.y)
        end = (goal.x, goal.y)

        if not kirby.health <= 40:
            optimal_path = astar(mapDraw, (start), end)

            if optimal_path:
                for position in optimal_path:
                    row, col = position
                    pathOptimize = pg.Surface((cell_width, cell_height), pg.SRCALPHA)
                    pg.draw.rect(pathOptimize, colorPath, (0, 0, cell_width, cell_height))
                    screen.blit(pathOptimize, (col * cell_width, row * cell_height))

        else:
            nearest_health_space = find_nearest_health_space((kirby.x, kirby.y), mapDraw)

            optimal_path = astar(mapDraw, (kirby.x, kirby.y), nearest_health_space, 5)

            if optimal_path:
                for position in optimal_path:
                    row, col = position
                    pathOptimize = pg.Surface((cell_width, cell_height), pg.SRCALPHA)
                    pg.draw.rect(pathOptimize, colorPath, (0, 0, cell_width, cell_height))
                    screen.blit(pathOptimize, (col * cell_width, row * cell_height))


def kirbyStatus():
    if kirby.health <= 0:
        kirby.health = 0
        kirby.alive = False
        screen.fill(BLACK)

    if kirby.health >= 100:
        kirby.health = 100


def draw_background():
    levelName = "Empty"

    match randomBG:
        case 0:
            levelName = "Moon"
            screen.blit(BGCOLOR, (0, 0))
        case 1:
            levelName = "Rainbow"
            screen.blit(BGCOLOR1, (0, 0))
        case 2:
            levelName = "Mansion"
            screen.blit(BGCOLOR2, (0, 0))
        case 3:
            levelName = "CAVE"
            screen.blit(BGCOLOR3, (0, 0))
        case 4:
            levelName = "VOLCANO"
            screen.blit(BGCOLOR4, (0, 0))
        case 5:
            levelName = "FOREST"
            screen.blit(BGCOLOR5, (0, 0))
        case 6:
            levelName = "OCEAN"
            screen.blit(BGCOLOR6, (0, 0))
        case 7:
            levelName = "MOUNTAINS"
            screen.blit(BGCOLOR7, (0, 0))
        case 8:
            levelName = "RUINS"
            screen.blit(BGCOLOR8, (0, 0))
        case 9:
            levelName = "GALAXY"
            screen.blit(BGCOLOR9, (0, 0))

    levelText = custom_font.render(levelName, True, (255, 255, 255))
    levelTextR = levelText.get_rect()
    levelTextR.center = (695, 45)
    screen.blit(levelText, levelTextR)


screen = pg.display.set_mode(SCREENSIZE)
pg.display.set_caption("Kirby And The AI")

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
                if paused or not kirby.alive:
                    finished = False
                    is_imposible = False
                    reset_game()
            elif event.key == pg.K_q:
                if not values_on and not paused and not error_validation:
                    values_on = True
                else:
                    values_on = False
            elif event.key == pg.K_s and not error_validation:
                if kirby.alive:
                    paused = not paused
                    if paused:
                        start_time = time.time() - auxTime

    if not draw_background():
        draw_background()

    if not paused:
        current_time = pg.time.get_ticks()
        if current_time - last_movement_time >= movement_interval:
            algorith()
            last_movement_time = current_time

        kirbyStatus()

        kirby.draw_health_bar(screen)
        hud.update()
        screen.blit(hud.image, (hud.rect.x, hud.rect.y))

        for row in range(10):
            for column in range(10):
                texture = None
                color = pg.Color(255, 255, 255, 25)

                if mapDraw[row][column] == 1:
                    texture = pg.image.load("resources/sprites/goal.png").convert_alpha()
                    texture = pg.transform.scale(texture, (52, 52))
                elif mapDraw[row][column] == 2:
                    texture = pg.image.load("resources/sprites/kirbySpriteD.png").convert_alpha()
                    texture = pg.transform.scale(texture, (52, 52))
                    if kirby.health == 0:
                        texture = pg.image.load("resources/sprites/KirbyDamage.png").convert_alpha()
                        texture = pg.transform.scale(texture, (52, 52))
                elif mapDraw[row][column] == 3:
                    texture = pg.image.load("resources/sprites/wallSprite.png").convert_alpha()
                    texture = pg.transform.scale(texture, (52, 52))
                elif mapDraw[row][column] == 4:
                    texture = pg.image.load("resources/sprites/damageS.png").convert_alpha()
                    texture = pg.transform.scale(texture, (52, 52))
                elif mapDraw[row][column] == 5:
                    texture = pg.image.load("resources/sprites/food.png").convert_alpha()
                    texture = pg.transform.scale(texture, (52, 52))

                if texture is not None:
                    screen.blit(texture, ((MARGIN + GRIDWIDTH) * column + MARGIN, (MARGIN + GRIDHEIGHT) * row + MARGIN))

                rect_surface = pg.Surface((GRIDWIDTH, GRIDHEIGHT), pg.SRCALPHA)
                pg.draw.rect(rect_surface, color, (0, 0, GRIDWIDTH, GRIDHEIGHT))

                screen.blit(rect_surface, ((MARGIN + GRIDWIDTH) * column + MARGIN,
                                           (MARGIN + GRIDHEIGHT) * row + MARGIN))

        drawUI()
        clock.tick(30)

    else:
        draw_pause_screen()

    pg.display.flip()

pg.quit()

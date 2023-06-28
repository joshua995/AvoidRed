"""
Joshua Liu
2-01-2023
"""

from time import time
from random import randint, uniform
from pygame import mixer

import SaveData

import pygame

pygame.init()

clock = pygame.time.Clock()

black, white, red, green, lightBlue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 100, 255)
yellow = (255, 255, 0)

WINDOW_SIZE, SPAWN_RANGE = 750, 200 # WINDOW_SIZE default 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Avoid Red"), screen.fill(black)

FONT_20 = pygame.font.SysFont('Arial', int(WINDOW_SIZE / 37.5))
FONT_30 = pygame.font.SysFont('Arial', int(WINDOW_SIZE / 25))
FONT_50 = pygame.font.SysFont('Arial', int(WINDOW_SIZE / 15))

halfWidth, halfHeight, = WINDOW_SIZE / 2, WINDOW_SIZE / 2

playerSize, playerPosition, playerSpeed, playerColor = 15, [halfWidth, halfHeight], 1.5, green

amountOfEnemies, amountOfBoosters, amountOfEliminators = int(WINDOW_SIZE / 37.5 / 4), int(WINDOW_SIZE / 93.75 / 4), 1

enemySize, enemyColor, enemyPositionsGoingDown, enemyPositionsGoingUp, enemyPositionsGoingRight = 10, red, [], [], []
enemySpeedsGoingDown, enemySpeedsGoingUp, enemySpeedsGoingRight, enemySpeedsGoingLeft = [], [], [], []
enemyPositionsGoingLeft = []

boosterSize, boosterColor, boosterSpeed, boosterPositionsGoingLeft = 10, green, 3, []
boosterPositionsGoingDown, boosterPositionsGoingUp, boosterPositionsGoingRight = [], [], []

eliminatorSize, eliminatorColor, eliminatorSpeed, eliminatorPositionsGoingLeft = 10, lightBlue, 2.5, []
eliminatorPositionsGoingDown, eliminatorPositionsGoingUp, eliminatorPositionsGoingRight = [], [], []

elementList = [enemyPositionsGoingDown, enemyPositionsGoingUp, enemyPositionsGoingRight, enemyPositionsGoingLeft,
               enemySpeedsGoingDown, enemySpeedsGoingUp, enemySpeedsGoingRight, enemySpeedsGoingLeft,
               boosterPositionsGoingDown, boosterPositionsGoingUp, boosterPositionsGoingRight,
               boosterPositionsGoingLeft, eliminatorPositionsGoingDown, eliminatorPositionsGoingUp,
               eliminatorPositionsGoingRight, eliminatorPositionsGoingLeft]

bonusSize, bonusPosition, bonusCollectedCount = 10, [0.0, 0.0], []

shieldActivatorSize, shieldActivatorPosition, isShieldActive, shieldSize = 12, [-100.0, -100.0], False, 25

isMovingUp, isMovingDown, isMovingRight, isMovingLeft = False, False, False, False

score, finalTime, finalScore, playAgainButtonSize = 0, 0, 0, [150, 50]
playAgainButtonPos, closeWindow, isGameOver = [halfWidth - 80, halfHeight + playAgainButtonSize[1] * 3], False, False

mixer.set_num_channels(5)
mixer.Channel(0).set_volume(.5)
mixer.Channel(0).play(mixer.Sound("Audio/Theme.mp3"), -1)


def generate_enemy_positions(position, speed, x_range, y_range):
    pos_x, pos_y = randint(x_range[0], x_range[1]), randint(y_range[0], y_range[1])
    position.append([pos_x, pos_y]), speed.append(0.01)


def generate_enemies():
    for _ in range(amountOfEnemies):
        generate_enemy_positions(elementList[0], elementList[4], [0, WINDOW_SIZE], [-SPAWN_RANGE, 0])
        generate_enemy_positions(elementList[1], elementList[5], [0, WINDOW_SIZE],
                                 [WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE])
        generate_enemy_positions(elementList[2], elementList[6], [-SPAWN_RANGE, 0], [0, WINDOW_SIZE])
        generate_enemy_positions(elementList[3], elementList[7], [WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE],
                                 [0, WINDOW_SIZE])


def map_draw_enemies(pos):
    rect = pygame.Rect(pos[0], pos[1], enemySize, enemySize)
    pygame.draw.rect(screen, enemyColor, rect)


def draw_enemies():
    list(map(map_draw_enemies, enemyPositionsGoingDown)), list(map(map_draw_enemies, enemyPositionsGoingUp))
    list(map(map_draw_enemies, enemyPositionsGoingRight)), list(map(map_draw_enemies, enemyPositionsGoingLeft))


def move_enemies():
    for i, pos in enumerate(enemyPositionsGoingDown):
        pos[1] += enemySpeedsGoingDown[i]
        if pos[1] > WINDOW_SIZE:
            pos[1], pos[0] = randint(-SPAWN_RANGE, 0), randint(0, WINDOW_SIZE)
        enemySpeedsGoingDown[i] += uniform(0.001, 0.005)
    for i, pos in enumerate(enemyPositionsGoingUp):
        pos[1] -= enemySpeedsGoingUp[i]
        if -enemySize > pos[1]:
            pos[1], pos[0] = randint(WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE), randint(0, WINDOW_SIZE)
        enemySpeedsGoingUp[i] += uniform(0.001, 0.005)
    for i, pos in enumerate(enemyPositionsGoingRight):
        pos[0] += enemySpeedsGoingRight[i]
        if pos[0] > WINDOW_SIZE:
            pos[0], pos[1] = randint(-SPAWN_RANGE * 2, 0), randint(0, WINDOW_SIZE)
        enemySpeedsGoingRight[i] += uniform(0.001, 0.005)
    for i, pos in enumerate(enemyPositionsGoingLeft):
        pos[0] -= enemySpeedsGoingLeft[i]
        if 0 > pos[0]:
            pos[0], pos[1] = randint(WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE * 2), randint(0, WINDOW_SIZE)
        enemySpeedsGoingLeft[i] += uniform(0.001, 0.005)


def generate_positions(position, x_range, y_range):
    pos_x, pos_y = randint(x_range[0], x_range[1]), randint(y_range[0], y_range[1])
    position.append([pos_x, pos_y])


def generate_boosters():
    for _ in range(amountOfBoosters):
        generate_positions(elementList[8], [0, WINDOW_SIZE], [-SPAWN_RANGE, 0])
        generate_positions(elementList[9], [0, WINDOW_SIZE], [WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE])
        generate_positions(elementList[10], [-SPAWN_RANGE, 0], [0, WINDOW_SIZE])
        generate_positions(elementList[11], [WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE], [0, WINDOW_SIZE])


def move_down_elements(position, speed):
    for pos in position:
        pos[1] += speed
        if pos[1] > WINDOW_SIZE:
            pos[1], pos[0] = randint(-SPAWN_RANGE, 0), randint(0, WINDOW_SIZE)


def move_up_elements(position, speed, size):
    for pos in position:
        pos[1] -= speed
        if pos[1] < -size:
            pos[1], pos[0] = randint(WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE), randint(0, WINDOW_SIZE)


def move_right_elements(position, speed):
    for pos in position:
        pos[0] += speed
        if pos[0] > WINDOW_SIZE:
            pos[0], pos[1] = randint(-SPAWN_RANGE, 0), randint(0, WINDOW_SIZE)


def move_left_elements(position, speed):
    for pos in position:
        pos[0] -= speed
        if pos[0] < 0:
            pos[0], pos[1] = randint(WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE), randint(0, WINDOW_SIZE)


def move_boosters():
    move_down_elements(elementList[8], boosterSpeed)
    move_up_elements(elementList[9], boosterSpeed, boosterSize)
    move_right_elements(elementList[10], boosterSpeed), move_left_elements(elementList[11], boosterSpeed)


def map_draw_boosters(pos):
    rect = pygame.Rect(pos[0], pos[1], boosterSize, boosterSize)
    pygame.draw.rect(screen, boosterColor, rect)


def draw_boosters():
    list(map(map_draw_boosters, elementList[8])), list(map(map_draw_boosters, elementList[9]))
    list(map(map_draw_boosters, elementList[10])), list(map(map_draw_boosters, elementList[11]))


def generate_eliminators():
    for _ in range(amountOfEliminators):
        generate_positions(elementList[12], [0, WINDOW_SIZE], [-SPAWN_RANGE, 0])
        generate_positions(elementList[13], [0, WINDOW_SIZE], [WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE])
        generate_positions(elementList[14], [-SPAWN_RANGE, 0], [0, WINDOW_SIZE])
        generate_positions(elementList[15], [WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE], [0, WINDOW_SIZE])


def move_eliminators():
    move_down_elements(elementList[12], eliminatorSpeed)
    move_up_elements(elementList[13], eliminatorSpeed, eliminatorSize)
    move_right_elements(elementList[14], eliminatorSpeed), move_left_elements(elementList[15], eliminatorSpeed)


def map_draw_eliminators(pos):
    rect = pygame.Rect(pos[0], pos[1], eliminatorSize, eliminatorSize)
    pygame.draw.rect(screen, eliminatorColor, rect)


def draw_eliminators():
    list(map(map_draw_eliminators, elementList[12])), list(map(map_draw_eliminators, elementList[13]))
    list(map(map_draw_eliminators, elementList[14])), list(map(map_draw_eliminators, elementList[15]))


def generate_bonus():
    bonusPosition[0], bonusPosition[1] = uniform(0, WINDOW_SIZE - bonusSize), uniform(0, WINDOW_SIZE - bonusSize)


def generate_shield_activator():
    shieldActivatorPosition[0] = uniform(0, WINDOW_SIZE - shieldActivatorSize)
    shieldActivatorPosition[1] = uniform(0, WINDOW_SIZE - shieldActivatorSize)


draw_bonus = lambda: pygame.draw.rect(screen, yellow, pygame.Rect(bonusPosition[0], bonusPosition[1], bonusSize,
                                                                  bonusSize))

draw_shield = lambda: pygame.draw.rect(screen, green, pygame.Rect(playerPosition[0] - 5, playerPosition[1] - 5,
                                                                  shieldSize, shieldSize), 2)

draw_shield_activator = lambda: pygame.draw.rect(screen, green,
                                                 pygame.Rect(shieldActivatorPosition[0], shieldActivatorPosition[1],
                                                             shieldActivatorSize, shieldActivatorSize), 2)


def move_and_draw_player():
    if isMovingRight and playerPosition[0] + playerSpeed < WINDOW_SIZE - playerSize:
        playerPosition[0] += playerSpeed
    elif isMovingLeft and playerPosition[0] + playerSpeed > 0:
        playerPosition[0] -= playerSpeed
    if isMovingUp and playerPosition[1] + playerSpeed > 0:
        playerPosition[1] -= playerSpeed
    elif isMovingDown and playerPosition[1] + playerSpeed < WINDOW_SIZE - playerSize:
        playerPosition[1] += playerSpeed
    player_rect = pygame.Rect(playerPosition[0], playerPosition[1], playerSize, playerSize)
    pygame.draw.rect(screen, playerColor, player_rect)


def collision_detection(p_pos, element_pos, e_size, p_size, value):
    for e_pos in element_pos:
        player_rect = pygame.Rect(p_pos[0], p_pos[1], p_size, p_size)
        element_rect = pygame.Rect(e_pos[0], e_pos[1], e_size, e_size)
        if pygame.Rect.colliderect(player_rect, element_rect):
            if value == 3:
                generate_bonus(), bonusCollectedCount.append(1)
                generate_shield_activator() if sum(bonusCollectedCount) % 3 == 0 else ''
            else:
                e_pos[0] = randint(WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE * 2)
            return True, value
    return False, 0


def reset_positions(down, up, right, left):
    for i, pos in enumerate(down):
        pos[1], pos[0] = randint(-SPAWN_RANGE, 0), randint(0, WINDOW_SIZE)
    for i, pos in enumerate(up):
        pos[1], pos[0] = randint(WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE), randint(0, WINDOW_SIZE)
    for i, pos in enumerate(right):
        pos[0], pos[1] = randint(-SPAWN_RANGE, 0), randint(0, WINDOW_SIZE)
    for i, pos in enumerate(left):
        pos[0], pos[1] = randint(WINDOW_SIZE, WINDOW_SIZE + SPAWN_RANGE), randint(0, WINDOW_SIZE)


def create_text_object(font, text, color, pos_x, pos_y, set_position):
    text = font.render(text, True, pygame.Color(color[0], color[1], color[2], 0))
    text_rect = text.get_rect()
    if set_position:
        text_rect.center = (pos_x, pos_y)
    screen.blit(text, text_rect)


def create_play_again_button():
    play_again_button_rect = pygame.Rect(playAgainButtonPos[0], playAgainButtonPos[1], playAgainButtonSize[0],
                                         playAgainButtonSize[1])
    pygame.draw.rect(screen, green, play_again_button_rect)
    create_text_object(FONT_30, "PLAY AGAIN", black, playAgainButtonPos[0] + playAgainButtonSize[0] / 2,
                       playAgainButtonPos[1] + playAgainButtonSize[1] / 2, True)


def reset_game():
    [position.clear() for position in elementList], generate_enemies(), generate_boosters(), generate_eliminators()
    return 0, 0, 1.5, [], False, [-100, 100]


if __name__ == "__main__":
    startTime = time()
    generate_enemies(), generate_boosters(), generate_eliminators(), generate_bonus()
    while not closeWindow:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                [mixer.Channel(i).stop() for i in range(1, 5)]
                closeWindow = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if event.button == 1 and isGameOver:
                    if playAgainButtonPos[0] + playAgainButtonSize[0] >= mousePos[0] >= playAgainButtonPos[0] and \
                            playAgainButtonPos[1] + playAgainButtonSize[1] >= mousePos[1] >= playAgainButtonPos[1]:
                        mixer.Channel(1).set_volume(1), mixer.Channel(1).play(mixer.Sound("Audio/Click.wav"))
                        startTime = time()
                        score, finalScore, playerSpeed, bonusCollectedCount, isShieldActive, shieldActivatorPosition = \
                            reset_game()
                        isGameOver = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    isMovingRight = True
                if event.key == pygame.K_LEFT:
                    isMovingLeft = True
                if event.key == pygame.K_UP:
                    isMovingUp = True
                if event.key == pygame.K_DOWN:
                    isMovingDown = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    isMovingRight = False
                if event.key == pygame.K_LEFT:
                    isMovingLeft = False
                if event.key == pygame.K_UP:
                    isMovingUp = False
                if event.key == pygame.K_DOWN:
                    isMovingDown = False
        if not isGameOver:
            move_and_draw_player(), move_enemies(), draw_enemies(), move_boosters(), draw_boosters(), draw_bonus()
            draw_shield_activator(), move_eliminators(), draw_eliminators()
            boosterHit = collision_detection(playerPosition, elementList[8] + elementList[9] + elementList[10] +
                                             elementList[11], boosterSize, playerSize, 1)
            eliminatorHit = collision_detection(playerPosition, elementList[12] + elementList[13] + elementList[14] +
                                                elementList[15], eliminatorSize, playerSize, 2)
            bonusHit = collision_detection(playerPosition, [bonusPosition], bonusSize, playerSize, 3)
            shieldActivatorHit = collision_detection(playerPosition, [shieldActivatorPosition], shieldActivatorSize,
                                                     playerSize, 1)
            if collision_detection(playerPosition, elementList[0] + elementList[1] + elementList[2] + elementList[3],
                                   enemySize, playerSize, 0)[0]:
                mixer.Channel(4).set_volume(1), mixer.Channel(4).play(mixer.Sound("Audio/Celebration.mp3"))
                isGameOver, finalTime = True, int(time() - startTime)
                if score > 0:
                    finalScore = score * finalTime
                elif score == 0:
                    finalScore = finalTime
            elif boosterHit[0]:
                playerSpeed += 0.025
                score += boosterHit[1]
            elif eliminatorHit[0]:
                mixer.Channel(2).set_volume(.8), mixer.Channel(2).play(mixer.Sound("Audio/Freeze.ogg"))
                reset_positions(elementList[0], elementList[1], elementList[2], elementList[3])
                reset_positions(elementList[8], elementList[9], elementList[10], elementList[11])
                reset_positions(elementList[12], elementList[13], elementList[14], elementList[15])
                score += eliminatorHit[1]
            if bonusHit[0]:
                score += bonusHit[1]
            if shieldActivatorHit[0] and not isShieldActive:
                mixer.Channel(3).set_volume(1), mixer.Channel(3).play(mixer.Sound("Audio/Shield.mp3"))
                isShieldActive = True
                shieldActivatorPosition = [-100.0, -100.0]
            if isShieldActive:
                draw_shield()
                if collision_detection([playerPosition[0] - 5, playerPosition[1] - 5],
                                       elementList[0] + elementList[1] + elementList[2] + elementList[3],
                                       enemySize, shieldSize, 0)[0]:
                    mixer.Channel(3).play(mixer.Sound("Audio/Shield.mp3"))
                    isShieldActive = False
            create_text_object(FONT_20, f"Time Alive {int(time() - startTime)}", green, 0, 0, False)
            create_text_object(FONT_20, f"Score {score}", green, halfWidth, 10, True)
        else:
            create_text_object(FONT_50, f"Game Over!!!".upper(), red, halfWidth, halfHeight - WINDOW_SIZE / 9.375,
                               True)
            create_text_object(FONT_30, f"Final Score {finalScore}".upper(), yellow, halfWidth, halfHeight, True)
            create_text_object(FONT_30, f"Score {score}", yellow, halfWidth, halfHeight + WINDOW_SIZE / 15, True)
            create_text_object(FONT_30, f"Time Alive {finalTime}", yellow, halfWidth, halfHeight + WINDOW_SIZE / 7.5,
                               True)
            create_play_again_button()
            longestTime, highestScore = SaveData.read_data()
            if longestTime < finalTime:
                longestTime = finalTime
            if highestScore < finalScore:
                highestScore = finalScore
            create_text_object(FONT_50, f"Best Score {highestScore}".upper(), yellow, halfWidth, WINDOW_SIZE / 7.5,
                               True)
            create_text_object(FONT_50, f"Longest Time Alive {longestTime}".upper(), yellow, halfWidth,
                               WINDOW_SIZE / 3.7, True)
            SaveData.write_data(longestTime, highestScore)
        clock.tick(60)
        pygame.display.update()

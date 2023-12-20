# creating a game
import pygame
import random
import  math

from pygame import mixer
from pygame import Surface, SurfaceType

# initialize game
pygame.init()

# add background music
mixer.music.load('y2mate.com - Fine line  Instrumental Slowed  Reverb.mp3')
mixer.music.play(-1)

# creating the window
Screen = pygame.display.set_mode((800, 600))

# set game name
pygame.display.set_caption("Mavundla's Game")

# change game icon
icon = pygame.image.load('WhatsApp Image 2022-02-24 at 4.51.32 PM.jpeg')
pygame.display.set_icon(icon)

# add the player in the game
playerImage = pygame.image.load('space-invaders.png')
playerRow = 300
playerColumn = 480
playerChangeX = 0
playerChangeY = 0

# add enemy in the game
enemy = []
enemyRow = []
enemyColumn = []
enemyChangeX = []
enemyChangeY = []
numberofEnemies = 4

# create multiple enemies
for i in range(numberofEnemies):
    enemy.append(pygame.image.load('ufolk .png'))
    enemyRow.append(random.randint(0,730))
    enemyColumn.append(random.randint(10,25))
    enemyChangeX.append(3)
    enemyChangeY.append(10)

# creating background image
background = pygame.image.load('background1.png')

# create bullets
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletState = "READY"
bulletSpeed = 10


# fire bullet function
def Fire_bullet(x, y):
    global bulletState
    bulletState = "FIRE"
    Screen.blit(bullet, (x + 16, y + 10))


def player(x, y):
    Screen.blit(playerImage, (x, y))


def enemyplayer(x, y, i):
    Screen.blit(enemy[i], (x, y))


# calculates for collusion
def collusiondetected(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Creating a score
score_value = 0
font = pygame.font.Font("Handwind.ttf", 45)
textX = 10
textY = 10

# function to display score
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    Screen.blit(score, (x, y))


# define game over
overFont = pygame.font.Font("Handwind.ttf", 64)

def game_over():
    overtext = overFont.render("GAME OVER", True, (255, 255, 255))
    Screen.blit(overtext, (200, 250))

# define win stage


winFont = pygame.font.Font("Handwind.ttf", 64)


def win_game():
    win_text = font.render("YOU WON", True, (255, 255, 255))
    Screen.blit(win_text, (200,250))


# game loop
running = True
while running:

    # background color
    Screen.fill((0, 0, 0))
    # background image
    Screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # moving the player using keys left or right
        # if the keyboard is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChangeX = -1.9
            if event.key == pygame.K_RIGHT:
                playerChangeX = 1.9
            if event.key == pygame.K_UP:
                playerChangeY = -0.1
            if event.key == pygame.K_DOWN:
                playerChangeY = 0.1
            # if space key is pressed the bullet will be fired when the bullet is ready
            if event.key == pygame.K_SPACE:
                if bulletState == "READY":
                    bulletX = playerRow
                    Fire_bullet(bulletX, bulletY)
        # if they keyboard is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerChangeX = -1.9
            if event.key == pygame.K_RIGHT:
                playerChangeX = 1.9

    # update movement
    playerRow += playerChangeX

    # move enemy
    for i in range(numberofEnemies):
        # set game over
        if enemyColumn[i] > 440:
            enemyColumn[i] = 2000
            game_over()
            break
        enemyRow[i] += enemyChangeX[i]

        if enemyRow[i] <= 0:
            enemyChangeX[i] = 3
            enemyColumn[i] += enemyChangeY[i]
        elif enemyRow[i] >= 730:
            enemyChangeX[i]= -3
            enemyColumn[i] += enemyChangeY[i]

        # check for collusion
        collusion = collusiondetected(enemyRow[i], enemyColumn[i], bulletX, bulletY)
        if collusion:
            bulletY = 480
            bulletState = "READY"
            score_value += 5
            enemyRow[i] = random.randint(0, 730)
            enemyColumn[i] = random.randint(10, 25)

        # place enemy
        enemyplayer(enemyRow[i], enemyColumn[i], i)

    # bullet state is ready to fire
    if bulletY <= 0:
        bulletY = 480
        bulletState = "READY"
    # fire bullet if bullet state is now fire
    if bulletState == "FIRE":
        Fire_bullet(bulletX, bulletY)
        bulletY -= bulletSpeed

    # create bounderies so the player does not move outside the area
    if playerRow <= 0:
        playerRow = 0
    if playerRow >= 730:
        playerRow = 730

    # place player
    player(playerRow, playerColumn)

    # cast score on screen
    show_score(textX, textY)

    # update game
    pygame.display.update()

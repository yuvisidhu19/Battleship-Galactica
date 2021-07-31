#How to play: Use left and right arrow keys to move the battleship and 'space' to shoot laser. If the aliens reach the same level as your spaceship, the game will be over. Score is displayed on the top left screen

import pygame
import random
from pygame import mixer

#COORDINATES IN THE SCREEN (DIRECTION): ----> (rightwards increases (x)) and DOWNWARDS (y) (increases)

#initialize pygame
pygame.init()                       #IMPORTANT

#box of the game
window = pygame.display.set_mode((800, 600))        #(x, y)

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('arcade.png')   #'load' loads the image in a variable. P.S.: Locaton of image(add r before it) if it is not inside folder. 32 pixel
pygame.display.set_icon(icon)

#background image
backgroundIMG = pygame.image.load('i01_background2.jpg')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)    #-1 = loop for music

#player
playerIMG = pygame.image.load('battleship.png')   #Locaton of image(add r before it) 64 pixel
playerX = 370
playerY = 480
change_x = 0
change_y = 0

def player(x, y):
    window.blit(playerIMG, (x, y))      #'blit' draws image on screen. x and y are coordinates

#enemy
num_of_enemies = 6
enemyIMG = []
enemyX = []
enemyY = []
enemychange_x = []
enemychange_y = []
for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load('ufo.png'))   #Locaton of image(add r before it) 64 pixel
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemychange_x.append(0.5)
    enemychange_y.append(60)

def enemy(x, y, i):
    window.blit(enemyIMG[i], (x, y))      #'blit' draws image on screen. x and y are coordinates

#laser
laserIMG = pygame.image.load('laser.png')   #Locaton of image(add r before it) 32 pixel
laserX = 370
laserY = 480
laserchange_x = 0
laserchange_y = -1
laser_state_fire = False

def laser(x, y):
    window.blit(laserIMG, (x, y))      #'blit' draws image on screen. x and y are coordinates

#collision
def collision(laserX, laserY, enemyX, enemyY):
    distance = ((laserX - enemyX)**2 + (laserY - enemyY)**2)**0.5     #formula of distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    if distance < 40:
        return True
    else:
        return False

#score
score_value = 0
font = pygame.font.SysFont('timesnewroman', 30, True)
scoreX = 12
scoreY = 10
def display_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    window.blit(score, (x, y))

#game over
font_gameover = pygame.font.SysFont('timesnewroman', 60, True)
def display_gameover():
    game_over_text = font_gameover.render('GAME OVER', True, (180, 0, 0))
    window.blit(game_over_text, (200, 250))

#game loop
running = True
while running:
    window.fill((62, 180, 137))         #RGB value (mint green) (in case u don't want any background image, u can colour background using this)
    window.blit(backgroundIMG, (0, 0))

    for input in pygame.event.get():    #Here, event detects any input
        if input.type == pygame.QUIT:
            running = False
        if input.type == pygame.KEYDOWN:    #keydown = key is pressed
            if input.key == pygame.K_LEFT:
                change_x -= 0.5
            if input.key == pygame.K_RIGHT:
                change_x += 0.5
            # if input.key == pygame.K_DOWN:
            #     change_y += 0.5
            # if input.key == pygame.K_UP:
            #     change_y -= 0.5
            if input.key == pygame.K_SPACE and laserY == playerY:
                laser_state_fire = True
                laserX = playerX + 15
                laser_sound = mixer.Sound('laser.wav')
                laser_sound.play()
        if input.type == pygame.KEYUP:      #keyup = key is released
            if input.key == pygame.K_LEFT or input.key == pygame.K_RIGHT:
                change_x = 0
            if input.key == pygame.K_DOWN or input.key == pygame.K_UP:
                change_y = 0

    #player
    playerX += change_x
    playerY += change_y
    player(playerX, playerY)
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:              #800(screen width) pixels - 64(image of spaceship is 64x64) pixels
        playerX = 736
    if playerY <= 0:
        playerY = 0
    if playerY >= 536:              #600-64 = 536
        playerY = 536

    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 430:
            for i in range(num_of_enemies):
                enemyY[i] = 2000
            display_gameover()
            break

        #enemy
        enemy(enemyX[i], enemyY[i], i)
        enemyX[i] += enemychange_x[i]
        #enemyY += enemychange_y
        if enemyX[i] >= 736:
            enemychange_x[i] = -0.5
            enemyY[i] += enemychange_y[i]
        if enemyX[i] <= 0:
            enemychange_x[i] = 0.5
            enemyY[i] += enemychange_y[i]

        #collision
        if collision(laserX, laserY, enemyX[i], enemyY[i]) and laser_state_fire:
            laser_state_fire = False
            laserY = 480
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 200)
            score_value += 1
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()

    #laser
    if laser_state_fire:
        laser(laserX, laserY)
        laserY += laserchange_y
        if laserY <= 0:
            laser_state_fire = False
            laserY = 480

    
    #score
    display_score(scoreX, scoreY)

    pygame.display.update()         #IMPORTANT


import pygame
import random
import math

#adding sounds to the game
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('stars.jpg')
#background sound
mixer.music.load('newbck1.wav')
mixer.music.play(-1)
# title and logo
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load('ufoo.png')
pygame.display.set_icon(icon)
# player
playerimg = pygame.image.load('spaceship.png')
playerx = 370
playery = 480
playerX_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('ufo1.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"  # ready to fire

# bullet
score_value = 0
font = pygame.font.Font('Waffle Crisp.ttf', 32)

textx = 10
texty = 10

#gameover_text
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text=over_font.render("Game Over".upper(),True,(255,255,255))
    screen.blit(over_text,(200,250))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


# collsion
def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
    if distance < 27:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerimg, (x, y))  # to draw the player img on the screen


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))  # to draw the player img on the screen


# holds the game window till close button is pressed
running = True
# infinite loop
while running:
    # to assign a background color
    screen.fill((0, 0, 0))
    # hold backgrounimage
    screen.blit(background, (0, 0))
    # player movement
    # playerx is reffering to the x coordinate and player y reffers to the y coordinate
    # and by increasing and decreasing the size of playerx and playery we can make our player move
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:  # KEYDOWN means pressing that key
            if event.key == pygame.K_LEFT:
                playerX_change -= 0.5
            if event.key == pygame.K_RIGHT:
                playerX_change += 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound('bulletfiring.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:  # KEYDOWN means pressing that key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerx += playerX_change
    # to add boundaries
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    enemyx += enemyX_change
    # enemy movement
    for i in range(num_of_enemies):

        #game over
        if enemyy[i]>440:
            for j in range(num_of_enemies):
                enemyy[j]=2000
            game_over_text()
            break
        enemyx[i] += enemyX_change[i]
        if enemyx[i] <= 0:
            enemyX_change[i] = 0.3
            enemyy[i] += enemyY_change[i]
        elif enemyx[i] >= 736:
            enemyX_change[i] = -0.3
            enemyy[i] += enemyY_change[i]

        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i], i)
    # bullet movement
    # infinite bullet
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bulletY_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()

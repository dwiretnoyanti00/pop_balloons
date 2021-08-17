import pygame
import random
import math

# MEMULAI PYGAME
from pygame import mixer

pygame.init()

# MEMBUAT LAYAR DISPLAY
screen = pygame.display.set_mode((900, 600))

# BACKGROUND
background = pygame.image.load('assets/cape.png')

# Background music
mixer.music.load('sounds/play_witme.mp3')
mixer.music.play(-1)

# JUDUL DAN IKON
pygame.display.set_caption("Pop the Balloons !!")
icon = pygame.image.load('assets/balloons.png')
pygame.display.set_icon(icon)

# PEMAIN (koordinat setengah dari display)
playerImg = pygame.image.load('assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# MUSUH
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/ballons.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# PANAH --ready belum nembak --fire menembak
arrowImg = pygame.image.load('assets/up-arrow.png')
arrowX = 0
arrowY = 480
arrowX_change = 0
arrowY_change = 10
arrow_state = "ready"

score_value = 0
font = pygame.font.Font('assets/PORKYS_.TTF', 32)
textX = 10
textY = 10

over_font=pygame.font.Font('assets/Top Secret.TTF', 64)

def show_score(x,y):
    score=font.render("Score : "+ str(score_value),True,(0,0,0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(0,0,0))
    screen.blit(over_text, (250, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def shoot_arrow(x, y):
    global arrow_state
    arrow_state = "fire"
    screen.blit(arrowImg, (x + 16, y + 10))


def function_collision(enemyX, enemyY, arrowX, arrowY):
    distance = math.sqrt(math.pow(enemyX - arrowX, 2) + (math.pow(enemyY - arrowY, 2)))
    if distance < 27:
        return True
    else:
        return False



# LOOP
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # CEK TOMBOL DIPENCET YANG KIRI ATAU KANAN
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if arrow_state == "ready":
                    explode_Sound=mixer.Sound('sounds/shoot.mp3')
                    explode_Sound.play()
                    # DAPATKAN KOORDINAT SEBELUMNYA
                    arrowX = playerX
                    shoot_arrow(playerX, arrowY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # ARTINYA 0 = STOP

    # BORDER BATAS KURSOR
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # PERGERAKAN BALON
    for i in range(num_of_enemies):

        # GAME OVER
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Tabrakan
        collision = function_collision(enemyX[i], enemyY[i], arrowX, arrowY)
        if collision:
            collision_Sound = mixer.Sound('sounds/pop.mp3')
            collision_Sound.play()
            arrowY = 480
            arrow_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # PERGERAKAN PANAH
    if arrowY <= 0:
        arrowY = 480
        arrow_state = "ready"
    if arrow_state == "fire":
        shoot_arrow(playerX, arrowY)
        arrowY -= arrowY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()

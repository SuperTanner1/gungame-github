import pygame
from pygame import mixer
import math
import random
pygame.init()

display_width = 1280            
display_height = 720
display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

# caption and background
background = pygame.image.load(".\\images\\background.png")
pygame.display.set_caption('New game')
icon = pygame.image.load(".\\images\\person.png")
pygame.display.set_icon(icon)

# background music
mixer.music.load(".\\sounds\\background.wav")
mixer.music.play(-1)
# Game over
font = pygame.font.Font("freesansbold.ttf", 32)
def game_over(x, y):
    gameover = font.render("Game Over", True, (255, 255, 255))
    display.blit(gameover, (x,y))

score_value = 0
def score(x, y):
    score_text = font.render("Score: " + str(score_value), True, (255, 255, 255))
    display.blit(score_text,(x, y))

score_milestones = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 50}

# Player
player_icon = pygame.image.load(".\\images\\person.png")
playerX = display_width * 0.2
playerY = display_height * 0.2
playerX_change = 0
playerY_change = 0
def player_place(x,y):
    display.blit(player_icon, (x,y))

# Gun
gun_icon = pygame.image.load(".\\images\\weapon.png")
gunX = display_width * 0.2
gunY = display_height * 0.2
gunX_change = 0
gunY_change = 0
def gun_place(x, y):
    display.blit(gun_icon, (x + 50,y+35))

# Bullet
bullet_icon = pygame.image.load(".\\images\\bullet.png")
bulletX = display_width * 0.8
bulletY = display_height + 64
bulletX_change = 0
bulletY_change = 0
bullet_state = "ready"
def fire_bullet(x , y):
    global bullet_state
    bullet_state = "fire"
    display.blit(bullet_icon, (x + 64, y + 32))

# enemy details
enemy_icon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 1
for i in range(num_of_enemies):
    enemy_icon.append(pygame.image.load('.\\images\\person.png'))
    enemyX.append(random.randint(display_width * 0.7, display_width - 64))
    enemyY.append(random.randint(1, display_height - 64))
    enemyX_change.append(0)
    enemyY_change.append(10)
def appendenemydetails(): # used for score effects
    global enemy_icon
    global enemyX
    global enemyY
    global enemyX_change
    global enemyY_change
    enemy_icon.append(pygame.image.load('.\\images\\person.png'))
    enemyX.append(random.randint(display_width * 0.7, display_width - 64))
    enemyY.append(random.randint(1, display_height - 64))
    enemyX_change.append(0)
    enemyY_change.append(10)


def enemy_place(x,y, i):
    display.blit(enemy_icon[i], (x,y))
def isCollision_bullet_enemy(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance < 20:
        return True
    else:
        return False
def isCollision_player_enemy(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt(math.pow(playerX - enemyX, 2) + math.pow(playerY - enemyY, 2))
    return distance
# game loop
running = True
while running:
    display.fill((0, 0, 0))
    display.blit(background, (0,0))
    score(10, 10)

    # Score effects try and except to stop false error breaking the game
    try:
        if score_value == score_milestones[1]:
            appendenemydetails()
            num_of_enemies += 1
            del score_milestones[1]
            print(score_milestones)
    except KeyError:
        pass
    try:
        if score_value == score_milestones[2]:
            appendenemydetails()
            num_of_enemies += 1
            del score_milestones[2]
            print(score_milestones)
    except KeyError:
        pass
    try:
        if score_value == score_milestones[3]:
            appendenemydetails()
            num_of_enemies += 1
            del score_milestones[3]
            print(score_milestones)
    except KeyError:
        pass
    try:
        if score_value == score_milestones[4]:
            appendenemydetails()
            num_of_enemies += 1
            del score_milestones[4]
            print(score_milestones)
    except KeyError:
        pass
    try:
        if score_value == score_milestones[5]:
            appendenemydetails()
            num_of_enemies += 1
            del score_milestones[5]
            print(score_milestones)
    except KeyError:
        pass
    try:
        if score_value == score_milestones[6]:
            if bulletX >= display_width - 100:
                bullet_state = "ready"
            del score_milestones[6]
            print(score_milestones)
    except KeyError:
        pass

# Game Loop
    for event in pygame.event.get():
        # Quit function for when player clicks the X button
        if event.type == pygame.QUIT:
            running = False
        # Tracks when arrow keys are pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change += 7
            if event.key == pygame.K_LEFT:
                playerX_change -= 7
            if event.key == pygame.K_UP:
                playerY_change -= 7
            if event.key == pygame.K_DOWN:
                playerY_change += 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound(".\\sounds\\pew.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    bullet_state = "fire"
        # Tracks when keys are let go
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_UP or pygame.K_DOWN:
                playerY_change = 0
    # Enemy movement
    for i in range(num_of_enemies):
        enemyY[i] += enemyY_change[i]
        if enemyY[i] >= display_height - 64:
            enemyX[i] -= 64
            enemyY_change[i] = -5
        if enemyY[i] <= 0:
            enemyX[i] -= 64
            enemyY_change[i] = 5
            # Collision
        collision_bullet_enemy = isCollision_bullet_enemy(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision_bullet_enemy == True:
            enemyX[i] = random.randint(display_width * 0.7, display_width - 64)
            enemyY[i] = random.randint(1, display_height - 64)
            bulletX = playerX
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
        collision_player_enemy = isCollision_player_enemy(playerX, playerY, enemyX[i], enemyY[i])
        if collision_player_enemy < 27 or enemyX[i] < 110:
            for j in range(num_of_enemies):
                enemyY[j] = 10000
            game_over(display_width * 0.5, display_height * 0.5)
            break
        enemy_place(enemyX[i], enemyY[i], i)

    # Bullet fire 
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletX_change = 20
    if bulletX >= display_width - 16:
        bulletX = playerX
        bullet_state = "ready"
    if bulletX <= 0:
        bulletX = playerX
        bullet_state = "ready"
    if bulletY >= display_height - 16:
        bulletY = playerY + 32
    if bulletY <= 0:
        bulletY = playerY + 32

    # Gun place
    gun_place(playerX, playerY)


    # Changes place of player and bullet
    playerX += playerX_change
    playerY += playerY_change
    bulletX += bulletX_change
    bulletY += bulletY_change

    player_place(playerX, playerY)
    clock.tick(60)
    pygame.display.update()

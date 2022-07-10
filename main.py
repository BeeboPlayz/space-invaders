from pdb import Restart
from time import time
from tracemalloc import start
import pygame
import random
from pygame import mixer

pygame.init() #intializes pygame

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1) #-1 loops music    

num_of_enemies = 16
speed = 0.1

gameOver = False
playing = False

screen = pygame.display.set_mode((800,600)) #creates the screen

#score

score_value = 0
font = pygame.font.Font("ka1.ttf",32)
font2 = pygame.font.Font("data-latin.ttf",32)
font3 = pygame.font.Font("data-latin.ttf",40)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render(f"Score: {score_value}",True,(25,100,255))
    screen.blit(score,(x,y))

#Game over text
over_font = pygame.font.Font("airstrike.ttf",64)
def game_over():
    global gameOver
    gameOver = True
    over_text = over_font.render(f"GAME OVER...",True,(200,0,0))
    restart_text = font2.render(f"[PRESS CTRL TO RESTART]",True,(180,0,0))
    screen.blit(over_text,(200,250))
    screen.blit(restart_text,(215,325))
    mixer.music.stop()

#background
background = pygame.image.load("background.jpg")

#edits display
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("spaceship.png")
playerXcord = 370
playerYcord = 440
playerXchange = 0

def player(x,y):
    screen.blit(playerImg,(x,y))

#enemy
enemyImg = []
enemyXcord = []
enemyYcord = []
enemyXchange = []
enemyYchange = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyXcord.append(random.randint(0,736))
    enemyYcord.append(random.randint(50,150))
    enemyXchange.append(speed)
    enemyYchange.append(40)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

#bullet
#ready = you cant see bullet
#fire = the bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletXcord = random.randint(0,736)
bulletYcord = 440
bulletXchange = 0
bulletYchange = 0.5
bulletState = "ready"

def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def startGame():
    font = pygame.font.Font("ka1.ttf",45)
    myText = font.render("CHOOSE YOUR DIFFICULTY:",True,(25,100,255))
    screen.blit(myText,(18,150))
    myText = font3.render("1) EASY 2) MEDIUM 3) HARD 4) EXTREME",True,(25,25,255))
    screen.blit(myText,(50,250))


def restartGame():
    global playing
    playing = False
    mixer.music.load("background.wav")
    mixer.music.play(-1) #-1 loops music
    for i in range(num_of_enemies):
        enemyYcord[i] = random.randint(50,150)

#makes sure game is always running
running = True
gameOn = False
while running:
    screen.fill((86,86,86))
    screen.blit(background,(0,0))
    if gameOn == False:
        startGame()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit detection
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -0.3
            if event.key == pygame.K_RIGHT:
                playerXchange = 0.3
            if event.key == pygame.K_1:
                diffMode = 1
                num_of_enemies = 4
                speed = 0.1
                gameOn = True
            if event.key == pygame.K_2:
                diffMode = 2
                num_of_enemies = 6
                speed = 0.2
                gameOn = True
            if event.key == pygame.K_3:
                diffMode = 3
                num_of_enemies = 8
                speed = 0.3
                gameOn = True
            if event.key == pygame.K_4:
                diffMode = 4
                num_of_enemies = 8
                speed = 0.3
                gameOn = True
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and bulletState == "ready":
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                bulletXcord = playerXcord
                fire_bullet(bulletXcord,bulletYcord)
            if (event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL) and gameOver == True:
                score_value = 0
                restartGame()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0
    

    #checking bounderies of area
    playerXcord += playerXchange

    if playerXcord <= 0:
        playerXcord = 0
    elif playerXcord >= 736:
        playerXcord = 736

    bulletRect = pygame.Rect(bulletXcord,bulletYcord,64,64)

    if gameOn == True:

        for i in range(num_of_enemies):

            #Game over
            if enemyYcord[i] > 360: #def 360
                for j in range(num_of_enemies):
                    enemyYcord[j] = 2000
                if playing == False:
                    playing = True
                    sound2 = mixer.Sound("game_over.wav")
                    sound2.play()
                game_over()
                break

            enemyXcord[i] += enemyXchange[i]

            if enemyXcord[i] <= 0:
                enemyXchange[i] = speed
                enemyYcord[i] += enemyYchange[i]
            elif enemyXcord[i] >= 736:
                enemyXchange[i] = -speed
                enemyYcord[i] += enemyYchange[i]

            enemyRect = pygame.Rect(enemyXcord[i],enemyYcord[i],64,64)

            #bullet collides with enemy
            if bulletRect.colliderect(enemyRect):
                explosion = mixer.Sound("explosion.wav")
                explosion.play()
                bulletYcord = 440
                bulletState = "ready"
                score_value += 1
                sound1 = mixer.Sound("harderEnemies.wav")
                if score_value == 50 and diffMode == 4:
                    num_of_enemies += 4
                    speed += 0.2
                    sound1.play()
                elif score_value == 100 and diffMode == 4:
                    num_of_enemies += 4
                    speed += 0.3
                    sound1.play()
                enemyXcord[i] = random.randint(0,736)
                enemyYcord[i] = random.randint(50,150)

            enemy(enemyXcord[i],enemyYcord[i],i)

        #bullet movement
        if bulletYcord <= 0:
            bulletYcord = 440
            bulletState = "ready"
        if bulletState == "fire":
            fire_bullet(bulletXcord,bulletYcord)
            bulletYcord -= bulletYchange

        player(playerXcord,playerYcord)
        show_score(textX,textY)
    pygame.display.update()

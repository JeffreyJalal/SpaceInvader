import pygame
from pygame import mixer
import numpy as np

# Initialize the pygame
pygame.init()

# Create the screen
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

# Background Init

background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (800, 600))

# Background Sound
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

# Player Initialization
playerImg = pygame.image.load("images/player.png")
playerImgSize = playerImg.get_size()

# Center of player is at half screen width
playerX = screenWidth / 2 - playerImgSize[0] / 2

# Bottom of player is at 9/10th screen height
playerY = 9 / 10 * screenHeight - playerImgSize[1]

playerSpeed = 0.5
playerX_change = 0

# Enemmies Initialization
numOfEnnemies = 6

ennemyImg = []
ennemyImgSize = []
ennemyX = []
ennemyY = []
ennemyXSpeed = []
ennemyX_change = []
ennemyXDirection = []

for i in range(numOfEnnemies):
    # Ennemy Initialization
    ennemyImg.append(pygame.image.load("images/ennemy.png"))
    ennemyImgSize.append(ennemyImg[i].get_size())

    # Center of ennemy is random on x axis
    ennemyX.append(np.random.randint(0, screenWidth - ennemyImgSize[i][0]))

    # Top of ennemy is random in first quarter of screen height
    ennemyY.append(np.random.randint(0, 1 / 4 * screenHeight))

    ennemyXSpeed.append(0.2)
    ennemyYSpeed = 0

    ennemyX_change.append(0)
    ennemyY_change = 0

    ennemyXDirection.append(np.random.choice([1, -1]))

# Laser Initialization
laserImg = pygame.image.load("images/laser.png")
laserImgSize = laserImg.get_size()

# Center of laser is initially aligned with spaceship
laserX = playerX + 1 / 2 * playerImgSize[0] - 1 / 2 * laserImgSize[0]

# Bottom of laser is on top of spaceship
laserY = playerY + laserImgSize[1]

laserYSpeed = 1

# ready - can't see laser on screen
# fire - laser is currently moving
laserState = "ready"

# Score
scoreValue = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game Over text

overFont = pygame.font.Font("freesansbold.ttf", 64)


def showScore(x, y):
    score = font.render("Score : " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameOverText(x, y):
    overText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (x, y))


def drawPlayer(x, y):
    screen.blit(playerImg, (x, y))


def drawEnnemy(img, x, y):
    screen.blit(img, (x, y))


def fireLaser(x, y):
    global laserState
    laserState = "fire"
    screen.blit(laserImg, (x, y))


def isCollision(ennemyX, ennemyY, laserX, laserY):
    distance = np.sqrt(np.power(ennemyX - laserX, 2) + np.power(ennemyY - laserY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= playerSpeed
            if event.key == pygame.K_RIGHT:
                playerX_change += playerSpeed
            if event.key == pygame.K_SPACE:
                if laserState == "ready":
                    # Current location of spaceship
                    laserX = playerX + 1 / 2 * playerImgSize[0] - 1 / 2 * laserImgSize[0]
                    fireLaser(laserX, laserY)
                    laserSound = mixer.Sound("sounds/laser.wav")
                    laserSound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change += playerSpeed
            if event.key == pygame.K_RIGHT:
                playerX_change -= playerSpeed

    # Move player
    playerX += playerX_change

    # Checking for boundaries of spaceship
    # Left boundary
    playerX = max(playerX, 0)
    # Right boundary
    playerX = min(playerX, screenWidth - playerImgSize[0])

    # Ennemies movement
    for i in range(numOfEnnemies):

        # Game Over
        if ennemyY[i] > 400:
            for j in range(numOfEnnemies):
                ennemyY[j] = 2000
            gameOverText(200, 250)
            break

        # Ennemy Movement
        # Checking for boundaries of ennemy
        # Left boundary
        ennemyX[i] = max(ennemyX[i], 0)
        # Right boundary
        ennemyX[i] = min(ennemyX[i], screenWidth - ennemyImgSize[i][0])

        if ennemyX[i] in [0, screenWidth - ennemyImgSize[i][0]]:
            ennemyXDirection[i] *= -1
            ennemyY[i] += ennemyImgSize[i][1]

        ennemyX_change[i] = ennemyXDirection[i] * ennemyXSpeed[i]

        ennemyX[i] += ennemyX_change[i]

        # Collision
        ennemyXCenter = ennemyX[i] + 1 / 2 * ennemyImgSize[i][0]
        ennemyYCenter = ennemyY[i] + 1 / 2 * ennemyImgSize[i][1]
        laserXCenter = laserX + 1 / 2 * laserImgSize[0]
        laserYCenter = laserY + 1 / 2 * laserImgSize[1]
        collision = isCollision(ennemyXCenter, ennemyYCenter, laserXCenter, laserYCenter)
        if collision:
            collisionSound = mixer.Sound("sounds/explosion.wav")
            collisionSound.play()
            laserY = playerY + laserImgSize[1]
            laserState = "ready"
            scoreValue += 1

            # Respawn ennemy
            # Center of ennemy is random on x axis
            ennemyX[i] = np.random.randint(0, screenWidth - ennemyImgSize[i][0])

            # Top of ennemy is random in first quarter of screen height
            ennemyY[i] = np.random.randint(0, 1 / 4 * screenHeight)

        drawEnnemy(ennemyImg[i], ennemyX[i], ennemyY[i])

    # Laser movement
    if laserY <= 0:
        laserY = playerY + laserImgSize[1]
        laserState = "ready"

    if laserState is "fire":
        fireLaser(laserX, laserY)
        laserY -= laserYSpeed

    drawPlayer(playerX, playerY)

    showScore(textX, textY)

    pygame.display.update()

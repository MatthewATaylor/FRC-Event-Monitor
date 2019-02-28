# I know, this code is very poorly written.

import pygame
import datetime
import time

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TIME_BAR_HEIGHT = 300
eventTime = [0, 0, 0]
timeBarColor = [0, 0, 0]
previousSlideMillisTime = 0
sponsorsIndex = 0
isRunning = True

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("FRC Pit Monitor")
clock = pygame.time.Clock()
timeFont = pygame.font.SysFont("arial", 110)
sponsorFont = pygame.font.SysFont("arial", 60)

def setEventParameters():
    global eventTime
    pygame.display.quit()

    print("Event Hour: ", end = "")
    eventTime[0] = input()
    
    print("Event Minute: ", end = "")
    eventTime[1] = input()
    
    print("Alliance Color (choose 'blue' or 'red'): ", end = "")
    inputColor = input()
    global timeBarColor
    if inputColor == "blue":
        timeBarColor = [0, 0, 255]
    elif inputColor == "red":
        timeBarColor = [255, 0, 0]
    else:
        timeBarColor = [120, 120, 120]

    pygame.display.init()
    global window
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def getCurrentTime():
    currentHour = datetime.datetime.now().time().hour
    currentMinute = datetime.datetime.now().time().minute
    currentSecond = datetime.datetime.now().time().second

    currentTime = [currentHour, currentMinute, currentSecond]
    return currentTime

def displayTime():
    global eventTime
    deltaTime = [0, 0, 0]
    currentTime = getCurrentTime()

    for i in range(0, 3):
        deltaTime[i] = int(eventTime[i]) - int(currentTime[i])

    for i in reversed(range(1, 3)):
        if deltaTime[i] < 0:
            deltaTime[i - 1] -= 1
            deltaTime[i] += 60
    
    for i in range(0, 3):
        deltaTime[i] = str(deltaTime[i])

    global timeFont
    for i in range(0, 3):
        if len(deltaTime[i]) < 2:
            deltaTime[i] = "0" + deltaTime[i]
    eventTimeString = "Time to Next Event: " + deltaTime[0] + ":" + deltaTime[1] + ":" + deltaTime[2]
    eventTimeTextSurface = timeFont.render(eventTimeString, True, (0, 0, 0))

    eventTimeTextDimensions = {
        "width": timeFont.size(eventTimeString)[0],
        "height": timeFont.size(eventTimeString)[1]
    }

    global SCREEN_WIDTH
    global TIME_BAR_HEIGHT
    eventTimeTextPos = {
        "x": SCREEN_WIDTH / 2 - eventTimeTextDimensions["width"] / 2,
        "y": TIME_BAR_HEIGHT / 2 - eventTimeTextDimensions["height"] / 2
    }

    global window
    window.blit(eventTimeTextSurface, (eventTimeTextPos["x"], eventTimeTextPos["y"]))

def displaySponsors():
    SPONSOR_TEXT_Y = 475
    SPONSOR_TEXT_HEIGHT = 120

    sponsors = ["Acme of Hudson", "NASA Robotics Alliance Project Registration Grant", "Burton D. Morgan Foundation Extracurricular Support Grant"]

    global previousSlideMillisTime
    currentMillisTime = time.time()
    deltaTime = currentMillisTime - previousSlideMillisTime
    
    global sponsorsIndex
    if deltaTime > 1:
        previousSlideMillisTime = currentMillisTime
        if sponsorsIndex >= 2:
            sponsorsIndex = 0
        else:
            sponsorsIndex += 1

    global sponsorFont
    sponsorString = "Sponsors: " + sponsors[sponsorsIndex]
    sponsorTextSurface = sponsorFont.render(sponsorString, True, (0, 0, 0))

    global window
    global SCREEN_WIDTH
    pygame.draw.rect(window, (120, 120, 120), pygame.Rect(0, SPONSOR_TEXT_Y, SCREEN_WIDTH, SPONSOR_TEXT_HEIGHT))
    window.blit(sponsorTextSurface, (5, SPONSOR_TEXT_Y + SPONSOR_TEXT_HEIGHT / 2 - sponsorFont.size(sponsorString)[1] / 2))

while isRunning:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
            isRunning = False
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
            setEventParameters()
    
    # Draw
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (timeBarColor[0], timeBarColor[1], timeBarColor[2]), pygame.Rect(0, 0, SCREEN_WIDTH, TIME_BAR_HEIGHT))
    pygame.draw.rect(window, (0, 0, 150), pygame.Rect(0, TIME_BAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - TIME_BAR_HEIGHT))
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, TIME_BAR_HEIGHT, SCREEN_WIDTH, TIME_BAR_HEIGHT / 4))
    displayTime()
    displaySponsors()
    pygame.display.flip()
    
    clock.tick(60)
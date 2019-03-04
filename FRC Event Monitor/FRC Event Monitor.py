# I know, this code is very poorly written.

import pygame
import datetime
import time

eventTime = [0, 0, 0]
timeBarColor = [0, 0, 0]
previousSlideMillisTime = 0
sponsorsIndex = 0
isRunning = True

pygame.init()

screenInfo = pygame.display.Info()
SCREEN_WIDTH = screenInfo.current_w
SCREEN_HEIGHT = screenInfo.current_h
TIME_BAR_HEIGHT = 0.28 * SCREEN_HEIGHT
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("FRC Pit Monitor")

clock = pygame.time.Clock()
timeFont = pygame.font.SysFont("arial", int(0.06 * SCREEN_WIDTH))
sponsorFont = pygame.font.SysFont("arial", int(0.03 * SCREEN_WIDTH))
teamLogo = pygame.image.load("Resources/Hudson Hybrids Logo.png")
teamLogo = pygame.transform.scale(teamLogo, (int(0.21 * SCREEN_WIDTH), int(0.37 * SCREEN_HEIGHT)))
teamLogo = teamLogo.convert_alpha()

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
    
    if deltaTime[0] < 0:
        for i in range(0, 3):
            deltaTime[i] = 0

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
    global SCREEN_HEIGHT
    SPONSOR_TEXT_Y = 0.44 * SCREEN_HEIGHT
    SPONSOR_TEXT_HEIGHT = 0.11 * SCREEN_HEIGHT

    sponsors = ["Acme of Hudson", "NASA Robotics Alliance Project Registration Grant", "Burton D. Morgan Foundation Extracurricular Support Grant", "Thomas and Tracy Corpus", "Jeffrey and Angela Gotthardt", "Suzanne and Paul Westlake", "Ivo and Elizabeth Cavoili"]

    global previousSlideMillisTime
    currentMillisTime = time.time()
    deltaTime = currentMillisTime - previousSlideMillisTime
    
    global sponsorsIndex
    if deltaTime > 2:
        previousSlideMillisTime = currentMillisTime
        if sponsorsIndex >= len(sponsors) - 1:
            sponsorsIndex = 0
        else:
            sponsorsIndex += 1

    global sponsorFont
    sponsorString = "Sponsors: " + sponsors[sponsorsIndex]
    sponsorTextSurface = sponsorFont.render(sponsorString, True, (0, 0, 0))

    global window
    global SCREEN_WIDTH
    pygame.draw.rect(window, (50, 50, 120), pygame.Rect(0, SPONSOR_TEXT_Y, SCREEN_WIDTH, SPONSOR_TEXT_HEIGHT))
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
    pygame.draw.rect(window, (100, 100, 125), pygame.Rect(0, TIME_BAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - TIME_BAR_HEIGHT))
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, TIME_BAR_HEIGHT, SCREEN_WIDTH, TIME_BAR_HEIGHT / 4))
    window.blit(teamLogo, (SCREEN_WIDTH / 2 - teamLogo.get_width() / 2, 0.6 * SCREEN_HEIGHT))
    displayTime()
    displaySponsors()
    pygame.display.flip()
    
    clock.tick(60)
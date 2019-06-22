import pygame
import datetime
import time

eventTime = [0, 0, 0]
timeBarColor = [0, 0, 0]
previousSlideMillisTime = 0
sponsorsIndex = 0
isRunning = True
matchNumber = 0

pygame.init()

screenInfo = pygame.display.Info()
SCREEN_WIDTH = screenInfo.current_w
SCREEN_HEIGHT = screenInfo.current_h
TIME_BAR_HEIGHT = 0.28 * SCREEN_HEIGHT
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("FRC Pit Monitor")

clock = pygame.time.Clock()
timeFont = pygame.font.SysFont("arial", int(0.035 * SCREEN_WIDTH))
matchFont = pygame.font.SysFont("arial", int(0.035 * SCREEN_WIDTH))
sponsorFont = pygame.font.SysFont("arial", int(0.03 * SCREEN_WIDTH))
teamNumFont = pygame.font.SysFont("arial", int(0.04 * SCREEN_WIDTH))
teamLogoWidth = 0.21 * SCREEN_WIDTH
teamLogo = pygame.image.load("Resources/Hudson Hybrids Logo.png")
teamLogo = pygame.transform.scale(teamLogo, (int(teamLogoWidth), int(0.37 * SCREEN_HEIGHT)))
teamLogo = teamLogo.convert_alpha()

def setEventParameters():
    global eventTime
    global matchNumber

    pygame.display.quit()

    print("Next Match Number: ", end = "")
    matchNumber = input()

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

    for i in range(0, 3):
        if len(deltaTime[i]) < 2:
            deltaTime[i] = "0" + deltaTime[i]
    eventTimeString = "Time to Next Match: " + deltaTime[0] + ":" + deltaTime[1] + ":" + deltaTime[2]
    eventTimeTextSurface = timeFont.render(eventTimeString, True, (0, 0, 0))

    eventTimeTextDimensions = {
        "width": timeFont.size(eventTimeString)[0],
        "height": timeFont.size(eventTimeString)[1]
    }

    eventTimeTextPos = {
        "x": SCREEN_WIDTH * 10 / 1920,
        "y": TIME_BAR_HEIGHT / 2 - eventTimeTextDimensions["height"] / 2
    }

    window.blit(eventTimeTextSurface, (eventTimeTextPos["x"], eventTimeTextPos["y"]))

def displayNextMatch():
    nextMatchNumberString = "Next Match Number: " + str(matchNumber)
    nextMatchNumberTextSurface = matchFont.render(nextMatchNumberString, True, (0, 0, 0))
    eventTimeTextWidth = timeFont.size("Time to Next Match: 00:00:00")[0]
    textX = eventTimeTextWidth + SCREEN_WIDTH * 150 / 1920
    textY = TIME_BAR_HEIGHT / 2 - matchFont.size(nextMatchNumberString)[1] / 2

    window.blit(nextMatchNumberTextSurface, (textX, textY))

def displaySponsors():
    SPONSOR_TEXT_Y = 0.44 * SCREEN_HEIGHT
    SPONSOR_TEXT_HEIGHT = 0.11 * SCREEN_HEIGHT

    sponsors = ["Acme of Hudson", "NASA Robotics Alliance Project Registration Grant", "Burton D. Morgan Foundation Extracurricular Support Grant", "Thomas and Tracy Corpus", "Jeffrey and Angela Gotthardt", "Suzanne and Paul Westlake", "Ivo and Elizabeth Cavoili", "Kathleen Owen Russell", "Firas and Melinda Al-Ali"]

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

    sponsorString = "Sponsors: " + sponsors[sponsorsIndex]
    sponsorTextSurface = sponsorFont.render(sponsorString, True, (0, 0, 0))

    pygame.draw.rect(window, (50, 50, 120), pygame.Rect(0, SPONSOR_TEXT_Y, SCREEN_WIDTH, SPONSOR_TEXT_HEIGHT))
    window.blit(sponsorTextSurface, (5, SPONSOR_TEXT_Y + SPONSOR_TEXT_HEIGHT / 2 - sponsorFont.size(sponsorString)[1] / 2))

def displayTeamNumber():
    teamNumString = "Team 7486"
    teamNumTextSurface = teamNumFont.render(teamNumString, True, (0, 0, 0))

    window.blit(teamNumTextSurface, (SCREEN_WIDTH / 2 + SCREEN_WIDTH * 80 / 1920, 0.6 * SCREEN_HEIGHT + 80))

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
    window.blit(teamLogo, (SCREEN_WIDTH / 2 - SCREEN_WIDTH * 90 / 1920 - teamLogoWidth, 0.6 * SCREEN_HEIGHT))
    displayTeamNumber()
    displayTime()
    displayNextMatch()
    displaySponsors()
    pygame.display.flip()
    
    clock.tick(60)

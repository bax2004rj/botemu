# Pygame
import math

import pygame

# Custom modules
import eventHandler
import fileHandler
import uiHandler

pygame.init()

#Audio setups
pygame.mixer.music.load(fileHandler.get_music())
game_over_sound = fileHandler.get_game_over_sound()
jump_sound = fileHandler.get_jump_sound()
pause_sound = fileHandler.get_pause_sound()
hover_sound = fileHandler.get_hover_sound()
click_sound = fileHandler.get_click_sound()


width = 1000
height = 600
screen = pygame.display.set_mode((1000,600),pygame.RESIZABLE)

pygame.display.set_caption("5842C bot emulator")
# Mouse setup
pygame.mouse.set_visible(False)
cursors = fileHandler.get_cursor_files()
cursors[0] = cursors[0].convert_alpha()
cursors[1] = cursors[1].convert_alpha()
cursor_state = 0
cursor_img_rect = cursors[cursor_state].get_rect()
playfieldRect = fileHandler.gameField.get_rect()
redHighGoalRect = fileHandler.redHighGoal.get_rect()
blueHighGoalRect = fileHandler.blueHighGoal.get_rect()
redLowGoalRect = fileHandler.redLowGoal.get_rect()
blueLowGoalRect = fileHandler.blueLowGoal.get_rect()

clock = pygame.time.Clock()
# Font files here
font_default = fileHandler.get_font_default()
font_big = fileHandler.get_font_big()
font_small = fileHandler.get_font_small()

compMode = False
gameStageText = "Auton"
gameStage = 0 # Game stage 0 = Auton, 1 = DriverControl, 2 = Endgame
minutesRemaining = 2
secondsRemaining = 59
modeMinutesRemaining = 0
modeSecondsRemaining = 15
recordMin = 0
recordSec = 00
zoomScale = 100

# Field movement: Mouse
panStartX = 0
panStartY = 0
dragging = False
dragStartx = 0
dragStarty = 0
panOffsetX = 0
panOffsetY = 0

# Field movement: Keyboard
moveFieldUp = False
moveFieldDown = False
moveFieldLeft = False
moveFieldRight = False
zoomIn = False
zoomOut = False
moveRate = 1

# Bot positioning
defaultX = 450
defaultY = 725
botX = defaultX
botY = defaultY
botDir = 0
moveLeftSide = 0
moveRightSide = 0
moveLeft = 0
moveRight = 0

discX = [100,200,300,400,500,600,700]
discY = [100,200,300,400,500,600,700]


# Button definitions here
fileButton = uiHandler.Button(font_small,30,24,0,0,1,text="File",button_type="procedural",active=True)
editButton = uiHandler.Button(font_small,30,24,30,0,1,text="Edit",button_type="procedural",active=True)
viewButton = uiHandler.Button(font_small,30,24,60,0,1,text="View",button_type="procedural",active=True)
gameButton = uiHandler.Button(font_small,30,24,90,0,1,text="Game",button_type="procedural",active=True)
aiButton = uiHandler.Button(font_small,20,24,120,0,1,text="AI",button_type="procedural",active=True)
timerButton = uiHandler.Button(font_small,35,24,140,0,1,text="Timer",button_type="procedural",active=True)
recButton = uiHandler.Button(font_small,50,24,width-200,0,1,text="REC: --:--",button_type="procedural",active=True,text_color="#ff0000")

# Window definitions here
performanceWin = uiHandler.window(screen,"Performance",(25,100,200,400),False,False,"#0050cf",True)
posWin = uiHandler.window(screen,"Positions",(50,125,200,400),True,False,"#5000cf",True)

#Variables
get_ticks_last_frame = 0
# Game scores: High goal
botHeldDisks = 0
redHighGoalDisks = 0
blueHighGoalDisks = 0
# Game scores: Low goal
redLowGoalDisks = 0
blueLowGoalDisks = 0
# Game scores: Endgame Expansion
redEndgameTiles = 0
blueEndgameTiles = 0
# Game scores: Owned color roller (0:neutral(blue next),1:neutral(red next),2:blue claimed,3:red claimed)
ColorRoller1Custody = 0
ColorRoller2Custody = 0
ColorRoller3Custody = 0
ColorRoller4Custody = 0
bScore = 0
rScore = 0

autonTime = 15
driverControlTime = 165
matchTime = 180

timerRunning = False
totalSecondsRemaining = 180

mainTimer = pygame.time.set_timer(pygame.USEREVENT,1000)

framelimit = 60

controlMode = "tank"

def recordBotKeystrokes(events):
    global moveLeftSide
    global moveRightSide
    global moveLeft
    global moveRight
    if controlMode == "tank":
        if "up_key_down" in events:
            moveLeftSide = -512
        elif "down_key_down" in events:
            moveLeftSide = 512   
        elif "left_key_down" in events:
            moveLeft = 512
        elif "right_key_down" in events:
            moveRight = 512
        elif "right_side_up_down" in events:
            moveRightSide = -512
        elif "right_side_down_down" in events:
            moveRightSide = 512
        elif "up_key_up" in events:
            moveLeftSide = 0
        elif "down_key_up" in events:
            moveLeftSide = 0    
        elif "left_key_up" in events:
            moveLeft = 0
        elif "right_key_up" in events:
            moveRight = 0
        elif "right_side_up_up" in events:
            moveRightSide = 0
        elif "right_side_down_up" in events:
            moveRightSide = 0

def displayPerformanceStats(screen,clock,win,events):
    if win.active:
        fps = clock.get_fps()
        fpsColor = "#ffffff"
        if fps > 30:
            fpsColor = "#00ff00"
        if fps <= 30 and fps >= 15:
            fpsColor = "#ffff00"
        else:
            fpsColor = "#ff0000"
        uiHandler.draw_text(screen,win.adjustedRectX+30,win.adjustedRectY+50,font_small,"FPS:%d"%fps,fpsColor)

def displayPositionStats(screen,clock,win,events):
    global botX
    global botY
    global botDir
    if win.active:
        uiHandler.draw_text(screen,win.adjustedRectX+30,win.adjustedRectY+50,font_small,"X:%d"%botX,"#FF0000")
        uiHandler.draw_text(screen,win.adjustedRectX+30,win.adjustedRectY+74,font_small,"Y:%d"%botY,"#00FF00")
        uiHandler.draw_text(screen,win.adjustedRectX+30,win.adjustedRectY+98,font_small,"Dir:%d"%botDir,"#0000FF")

while 1: # Main game loop
    # Get time, solve for FPS
    ticks = pygame.time.get_ticks()
    delta_time = (ticks - get_ticks_last_frame) / 1000.0
    get_ticks_last_frame = ticks
    # Get size of rect
    playfieldRect = fileHandler.gameField.get_rect()
    # Check for window resize
    width,height = screen.get_size()
    # Move record button based on window size
    recButton.button_box_rect.topleft = width-220,0
    recButton.outline_rect.topleft = width-220.5,0

    # Check for events
    events = eventHandler.get_events()
    # Get mouse info for updates
    cursor_img_rect.topleft = pygame.mouse.get_pos()
    # Check if quitting
    if "terminate" in events:
        pygame.quit()
        exit()
    elif "mouse_button_down" in events:
        if eventHandler.eventButton == 2:
            dragging = True
            dragStartx,dragStarty = eventHandler.eventPos
            panStartX = panOffsetX - dragStartx
            panStartY = panOffsetY - dragStarty
    elif "mouse_button_up" in events:
        dragging = False
    elif "mouse_motion" in events:
        if dragging == True:
            dragStartx,dragStarty = eventHandler.eventPos
            panOffsetX = dragStartx + panStartX
            panOffsetY = dragStarty + panStartY
    elif "fieldUp_down" in events:
        moveFieldUp = True
    elif "fieldLeft_down" in events:
        moveFieldLeft = True
    elif "fieldRight_down" in events:
        moveFieldRight = True
    elif "fieldDown_down" in events:
        moveFieldDown = True
    elif "fieldZoomIn_down" in events:
        zoomIn = True
    elif "fieldZoomOut_down" in events:
        zoomOut = True
    elif "fieldUp_up" in events:
        moveFieldUp = False
    elif "fieldLeft_up" in events:
        moveFieldLeft = False
    elif "fieldRight_up" in events:
        moveFieldRight = False
    elif "fieldDown_up" in events:
        moveFieldDown = False
    elif "fieldZoomIn_up" in events:
        zoomIn = False
    elif "fieldZoomOut_up" in events:
        zoomOut = False
    elif "mouseWheel" in events and eventHandler.scrollAmount > 0 and zoomScale<1000:
        zoomScale +=1
        uiHandler.draw_text(screen,width/2,height/2,font_default,"Zoom: %d"%zoomScale,"#00FF87")
    elif "mouseWheel" in events and eventHandler.scrollAmount < 0 and zoomScale>10:
        zoomScale -=1
        uiHandler.draw_text(screen,width/2,height/2,font_default,"Zoom: %d"%zoomScale,"#00FF87")
    elif "space_down" in events:
        if not timerRunning:
            timerStart_ticks = pygame.time.get_ticks()
            timerRunning = True
        else:
            timerRunning = False
            totalSecondsRemaining = 180
    try:
        if eventHandler.control.joy_name == "":
            recordBotKeystrokes(events)
        else:
            moveLeftSide = eventHandler.control.axis_data[1]*512
            moveRightSide = eventHandler.control.axis_data[3]*512
    except AttributeError:
        recordBotKeystrokes(events)

    
    # Bot control simulation
    botDir += (moveLeftSide-moveRightSide)/256
    botRadians = math.radians(botDir-180)
    botX += -((moveLeftSide+moveRightSide)/256) * math.sin(botRadians)
    botY += -((moveLeftSide+moveRightSide)/256) * math.cos(botRadians)


    if timerRunning:
        if not totalSecondsRemaining == 0:
            totalSecondsRemaining = matchTime - math.floor((pygame.time.get_ticks()-timerStart_ticks)/1000)
        else:
            timerRunning = False
            totalSecondsRemaining = 180

    # Update and calculate scores TODO: Calculate endgame scores
    bScore = blueHighGoalDisks*5+blueLowGoalDisks
    if ColorRoller1Custody == 2: # May look weird, but this is to make sure all color rollers are accounted for
        bScore += 10
    if ColorRoller2Custody == 2:
        bScore += 10
    if ColorRoller3Custody == 2:
        bScore += 10
    if ColorRoller4Custody == 2:
        bScore += 10
    rScore = blueHighGoalDisks*5+blueLowGoalDisks
    if ColorRoller1Custody == 3: # May look weird, but this is to make sure all color rollers are accounted for
        rScore += 10
    if ColorRoller2Custody == 3:
        rScore += 10
    if ColorRoller3Custody == 3:
        rScore += 10
    if ColorRoller4Custody == 3:
        rScore += 10
    
    # Draw playfield
    screen.fill("#2f2f2f")
    # Scale objects
    scaledGameField = pygame.transform.scale(fileHandler.gameField,(playfieldRect.width*(zoomScale/100),playfieldRect.height*(zoomScale/100)))
    scaledDisc = pygame.transform.scale(fileHandler.disc,(playfieldRect.width*(zoomScale/100)*.05,playfieldRect.height*(zoomScale/100)*.05))
    scaledRedHighGoal = pygame.transform.scale(fileHandler.redHighGoal,(redHighGoalRect.width*(zoomScale/100)*.25,redHighGoalRect.height*(zoomScale/100)*.25))
    scaledBlueHighGoal = pygame.transform.scale(fileHandler.blueHighGoal,(blueHighGoalRect.width*(zoomScale/100)*.25,blueHighGoalRect.height*(zoomScale/100)*.25))
    scaledBlueLowGoal = pygame.transform.scale(fileHandler.blueLowGoal,(blueLowGoalRect.width*(zoomScale/100)*.275,blueHighGoalRect.height*(zoomScale/100)*.25))
    scaledRedLowGoal = pygame.transform.scale(fileHandler.redLowGoal,(blueLowGoalRect.width*(zoomScale/100)*.30,blueHighGoalRect.height*(zoomScale/100)*.25))
    scaledRedLowGoal = pygame.transform.rotate(scaledRedLowGoal,180)
    scaledFieldRect = scaledGameField.get_rect()
    # Draw game objects
    screen.blit(scaledGameField,(width/2+panOffsetX,height/2+panOffsetY))
    screen.blit(scaledBlueLowGoal,((width/2+panOffsetX)+(scaledFieldRect.width-(272*zoomScale/100)),(height/2+panOffsetY)+(132*zoomScale/100)))
    screen.blit(scaledRedLowGoal,((width/2+panOffsetX)+(132*zoomScale/100),(height/2+panOffsetY)+(scaledFieldRect.height-(275*zoomScale/100))))
    for i in range(len(discX)): #Uses length instead of values to support multiple disks at same position 
        discXI = discX[i]
        discYI = discY[i]
        screen.blit(scaledDisc,((discXI*zoomScale/100)+(width/2+panOffsetX),(discYI*zoomScale/100)+(height/2+panOffsetY)))
    # Draw bots before anything above it
    scaledRedBot = pygame.transform.scale(fileHandler.redbot,(32*(zoomScale/50),32*(zoomScale/50)))
    scaledRedBot = pygame.transform.rotate(scaledRedBot,botDir)
    screen.blit(scaledRedBot,((width/2+panOffsetX)+(botX*zoomScale/100),(height/2+panOffsetY)+(botY*zoomScale/100)))
    uiHandler.draw_text(screen,(width/2+panOffsetX)+((botX+32)*zoomScale/100),(height/2+panOffsetY)+((botY+32)*zoomScale/100),font_default,"%d"%botHeldDisks,"#FFFFFF")
    # High goals
    screen.blit(scaledRedHighGoal,((width/2+panOffsetX)+(scaledFieldRect.width-(160*zoomScale/100)),(height/2+panOffsetY)+(50*zoomScale/100)))
    screen.blit(scaledBlueHighGoal,((width/2+panOffsetX)+(50*zoomScale/100),(height/2+panOffsetY)+(scaledFieldRect.height-(160*zoomScale/100))))
    uiHandler.draw_text(screen,(width/2+panOffsetX)+(scaledFieldRect.width-(90*zoomScale/100)),(height/2+panOffsetY)+(114*zoomScale/100),font_default,"%d"%redHighGoalDisks,"#FFFFFF")
    uiHandler.draw_text(screen,(width/2+panOffsetX)+(114*zoomScale/100),(height/2+panOffsetY)+(scaledFieldRect.height-(90*zoomScale/100)),font_default,"%d"%blueHighGoalDisks,"#FFFFFF")
    # Draw top menu bar
    pygame.draw.rect(screen,(128,128,128),(0,0,width,24))
    fileButton.active = True
    fileButton.update(screen,cursor_img_rect,events)
    editButton.active = True
    editButton.update(screen,cursor_img_rect,events)
    viewButton.active = True
    viewButton.update(screen,cursor_img_rect,events)
    gameButton.active = True
    gameButton.update(screen,cursor_img_rect,events)
    aiButton.active = True
    aiButton.update(screen,cursor_img_rect,events)
    timerButton.active = True
    timerButton.update(screen,cursor_img_rect,events)
    recButton.active = True
    recButton.update(screen,cursor_img_rect,events)
    
    uiHandler.draw_text(screen,width/2-20,10,font_small,str(bScore),"#0000ff")
    uiHandler.draw_text(screen,width/2,10,font_small,"|","#870087")
    uiHandler.draw_text(screen,width/2+20,10,font_small,str(bScore),"#ff0000")
    minutesRemaining = math.floor(totalSecondsRemaining/60)
    secondsRemaining = totalSecondsRemaining-(minutesRemaining*60)
    
    if minutesRemaining >=2 and secondsRemaining >= 45:
        gameStage = 0
        gameStageText = "Auton"
        modeMinutesRemaining = 0
        modeSecondsRemaining = secondsRemaining-45
    elif minutesRemaining == 0 and secondsRemaining < 10:
        gameStage = 2
        gameStageText = "End/DC"
        modeMinutesRemaining = minutesRemaining
        modeSecondsRemaining = secondsRemaining
    else:
        gameStage = 1
        gameStageText = "Drive"
        modeMinutesRemaining = minutesRemaining
        modeSecondsRemaining = secondsRemaining

    if secondsRemaining>=10:
        addzero = ""
    else:
        addzero = "0"
    
    if modeSecondsRemaining>=10:
        addModeZero = ""
    else:
        addModeZero = "0"

    uiHandler.draw_text(screen,width-40,10,font_small,"Time: %d:%s%d"%(minutesRemaining,addzero,secondsRemaining),"#000000")
    uiHandler.draw_text(screen,width-110,10,font_small,"%s: %d:%s%d"%(gameStageText,modeMinutesRemaining,addModeZero,modeSecondsRemaining),"#000000")
    # Run window tasks
    displayPerformanceStats(screen,clock,performanceWin,events)
    displayPositionStats(screen,clock,posWin,events)
    # Draw windows
    posWin.update(screen,cursor_img_rect,events)
    performanceWin.update(screen,cursor_img_rect,events)
    # Render last so huds and displays can show overlays
    if moveFieldUp:
        panOffsetY += moveRate*zoomScale/100
    if moveFieldLeft:
        panOffsetX -= moveRate*zoomScale/100
    if moveFieldRight:
        panOffsetX += moveRate*zoomScale/100
    if moveFieldDown:
        panOffsetY -= moveRate*zoomScale/100
    if zoomIn and zoomScale<500:
        zoomScale += 1
        uiHandler.draw_text(screen,width/2,height/2,font_default,"Zoom: %d"%zoomScale,"#00FF87")
    if zoomOut and zoomScale>10:
        zoomScale -= 1
        uiHandler.draw_text(screen,width/2,height/2,font_default,"Zoom: %d"%zoomScale,"#00FF87")

    screen.blit(cursors[0], cursor_img_rect)
    pygame.display.flip()
    clock.tick(framelimit)


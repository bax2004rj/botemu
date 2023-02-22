# Pygame
import math
import pygame

# Custom modules
import eventHandler
import fileHandler
import uiHandler
import physicsHandler

#Other
import psutil

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

# Zoom data 
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
defaultX = 465
defaultY = 730
botX = defaultX
botY = defaultY
botDir = 0
moveLeftSide = 0
moveRightSide = 0
moveLeft = 0
moveRight = 0
intake = False
power = 0
angle = 40
addPwr = False

discX = physicsHandler.discX
discY = physicsHandler.discY
targetX = []
targetY = []
targetI = []
targetXInv = []
targetYInv = []

# Button definitions here
# Menu bar
fileButton = uiHandler.Button(font_small,30,24,0,0,1,text="File",button_type="procedural",active=True,box_color="#1f1f1f",text_color="#ffffff")
editButton = uiHandler.Button(font_small,30,24,30,0,1,text="Edit",button_type="procedural",active=True,box_color="#1f1f1f",text_color="#ffffff")
viewButton = uiHandler.Button(font_small,30,24,60,0,1,text="View",button_type="procedural",active=True,box_color="#1f1f1f",text_color="#ffffff")
gameButton = uiHandler.Button(font_small,30,24,90,0,1,text="Game",button_type="procedural",active=True,box_color="#1f1f1f",text_color="#ffffff")
aiButton = uiHandler.Button(font_small,20,24,120,0,1,text="AI",button_type="procedural",active=True,box_color="#1f1f1f",text_color="#ffffff")
timerButton = uiHandler.Button(font_small,35,24,140,0,1,text="Timer",button_type="procedural",active=True,box_color="#1f1f1f",text_color="#ffffff")
recButton = uiHandler.Button(font_small,50,24,width-200,0,1,text="REC: --:--",button_type="procedural",active=True,text_color="#ff0000",box_color="#1f1f1f")
#View Menu options
performanceButton = uiHandler.Button(font_small,100,24,60,24,1,text = "✓ Performance",box_color="#1f1f1f",text_color="#ffffff")
positionsButton = uiHandler.Button(font_small,100,24,60,48,1,text = "✓ Positions",box_color="#1f1f1f",text_color="#ffffff")
motorsButton = uiHandler.Button(font_small,100,24,60,72,1,text = "  Motors",box_color="#1f1f1f",text_color="#ffffff")
botConfigButton = uiHandler.Button(font_small,100,24,60,96,1,text = "  Bot config",box_color="#1f1f1f",text_color="#ffffff")
showPhysicsButton = uiHandler.Button(font_small,100,24,60,134,1,text = "  Show hitboxes",box_color="#1f1f1f",text_color="#ffffff")
# Timer menu options
compModeButton = uiHandler.Button(font_small,100,24,140,24,1,text = "✓ Comp",box_color="#1f1f1f",text_color="#ffffff")
autonSkillsButton = uiHandler.Button(font_small,100,24,140,48,1,text = "  Skills: Auton",box_color="#1f1f1f",text_color="#ffffff")
driverSkillsButton = uiHandler.Button(font_small,100,24,140,72,1,text = "  Skills: Driver",box_color="#1f1f1f",text_color="#ffffff")
noTimerButton = uiHandler.Button(font_small,100,24,140,96,1,text = "  Stopwatch",box_color="#1f1f1f",text_color="#ffffff")
runTimerButton = uiHandler.Button(font_small,100,24,140,144,1,text = "Run timer (space)",box_color="#1f1f1f",text_color="#ffffff")
# Bot config buttons
weaponConfig = uiHandler.checkButton(font_small,"High goal scoring","checkbox",[0,0,150,24],active = False)
ApplyButton = uiHandler.Button(font_small,70,24,80,24,1,text = "Apply",box_color="#1f3f6f",text_color="#ffffff",active=False)
CancelButton = uiHandler.Button(font_small,70,24,0,24,1,text = "Cancel",box_color="#1f1f1f",text_color="#ffffff",active=False)

fileOpen = False
editOpen = False
viewOpen = False
gameOpen = False
aiOpen = False
timerOpen = False
recOpen = False

# Window definitions here
performanceWin = uiHandler.window(screen,"Performance",(25,100,200,200),True,False,"#0050cf",True)
posWin = uiHandler.window(screen,"Positions",(25,300,200,150),True,False,"#5000cf",True)
motorWin = uiHandler.window(screen,"Motors",(25,450,200,150),True,False,"#870000",False)
botConfigWin = uiHandler.window(screen,"Bot Configuration",(250,250,400,200),True,False,"#008250",False)
# Color roller physics rect
colorRoller1Rect = pygame.Rect(554,784,48,16)
colorRoller2Rect = pygame.Rect(200,0,48,16)
colorRoller3Rect = pygame.Rect(0,154,16,48)
colorRoller4Rect = pygame.Rect(782,600,16,48)
blueLowGoalHitbox = pygame.Rect(532,268,268,268)
redLowGoalHitbox = pygame.Rect(0,800,268,268)
# Variables
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

timerMode = "comp"
timerRunning = False
totalSecondsRemaining = 180

mainTimer = pygame.time.set_timer(pygame.USEREVENT,1000)
colorRollerTimer = pygame.time.set_timer(pygame.USEREVENT+2,125)
timerStart_ticks = 0


framelimit = -1
fpsSpeedScale = 10
fps = 60

controlMode = "tank"

showPhysics = False

def recordBotKeystrokes(events,fps):
    global moveLeftSide
    global moveRightSide
    global moveLeft
    global moveRight
    global intake
    if controlMode == "tank":
        if "up_key_down" in events:
            moveLeftSide = -512/fps
        elif "down_key_down" in events:
            moveLeftSide = 512/fps
        elif "left_key_down" in events:
            moveLeft = 512/fps
        elif "right_key_down" in events:
            moveRight = 512/fps
        elif "right_side_up_down" in events:
            moveRightSide = -512/fps
        elif "right_side_down_down" in events:
            moveRightSide = 512/fps
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
        elif "run_intake" in events:
            intake = True
        elif "stop_intake" in events:
            intake = False

def displayPerformanceStats(screen,clock,win,events):
    global fpsSpeedScale
    if win.active:
        fps = clock.get_fps()
        fpsColor = "#ffffff"
        if fps > 30:
            fpsColor = "#00ff00"
        if fps <= 30 and fps >= 15:
            fpsColor = "#ffff00"
        if fps <15:
            fpsColor = "#ff0000"
            fps = clock.get_fps()
        cpu = psutil.cpu_percent()
        cpuColor = "#ffffff"
        uiHandler.draw_text(screen,(win.adjustedRectX+win.adjustedWidth)/2,win.adjustedRectY+30,font_small,"----Graphics----","#00ffff")
        uiHandler.draw_text(screen,(win.adjustedRectX+win.adjustedWidth)/2,win.adjustedRectY+50,font_small,"FPS:%d"%fps,fpsColor)
        uiHandler.draw_text(screen,(win.adjustedRectX+win.adjustedWidth)/2,win.adjustedRectY+90,font_small,"Viewport:%dx%d"%(width,height),"#FFFFFF")
        uiHandler.draw_text(screen,(win.adjustedRectX+win.adjustedWidth)/2,win.adjustedRectY+110,font_small,"Resolution:%dx%d"%(width,height),"#FFFFFF")
        uiHandler.draw_text(screen,win.adjustedRectX+100,win.adjustedRectY+70,font_small,"Movement scale:%f"%fpsSpeedScale,fpsColor)
        uiHandler.draw_text(screen,(win.adjustedRectX+win.adjustedWidth)/2,win.adjustedRectY+130,font_small,"Framelimit:%d"%(framelimit),"#FFFFFF")
        uiHandler.draw_text(screen,(win.adjustedRectX+win.adjustedWidth)/2,win.adjustedRectY+150,font_small,"-------CPU-------","#870087")
        uiHandler.draw_text(screen,(win.adjustedRectX+win.adjustedWidth)/2,win.adjustedRectY+170,font_small,"Usage:{0}".format(cpu),cpuColor)
        uiHandler.draw_text(screen,(win.adjustedRectX+win.adjustedWidth)/2,win.adjustedRectY+190,font_small,"Cores:{0}".format(psutil.cpu_count()),cpuColor)

def displayPositionStats(screen,clock,win,events):
    global botX
    global botY
    global botDir
    global power
    if win.active:
        uiHandler.draw_text(screen,win.adjustedRectX+30,win.adjustedRectY+50,font_small,"X:%d"%(botX+32),"#FF0000")
        uiHandler.draw_text(screen,win.adjustedRectX+30,win.adjustedRectY+74,font_small,"Y:%d"%(botY+32),"#00FF00")
        uiHandler.draw_text(screen,win.adjustedRectX+30,win.adjustedRectY+98,font_small,"Dir:%d"%botDir,"#0000FF")
        uiHandler.draw_text(screen,win.adjustedRectX+150,win.adjustedRectY+50,font_small,"Field X:%d"%panOffsetX,"#FFD0D0")
        uiHandler.draw_text(screen,win.adjustedRectX+150,win.adjustedRectY+74,font_small,"Field Y:%d"%panOffsetY,"#D0FFD0")
        uiHandler.draw_text(screen,win.adjustedRectX+150,win.adjustedRectY+125,font_small,"Zoom:%d"%zoomScale,"#00FF87")
        uiHandler.draw_text(screen,win.adjustedRectX+30,win.adjustedRectY+125,font_small,"Power:%d"%power,"#FFFFFF")

def displayMotorStats(screen, clock, win, events,lspeed,rspeed,power):
    global fpsSpeedScale
    if win.active:
        # Draw rectangles
        lcolR = 255
        lcolG = 0
        revl = 0
        rcolR = 255
        rcolG = 0
        revr = 0
        try:
            lcolR = abs(lspeed)/2
            lcolG = abs(lspeed)/2
            revl = 0
            if lspeed < 0:
                revl = 255
            rcolR = abs(lspeed)/2
            rcolG = abs(lspeed)/2
            revr = 0
            if rspeed > 0:
                revr = 255
        except ZeroDivisionError:
            lcolR = 255
            lcolG = 0
            revl = 0
        pygame.draw.rect(screen,(lcolR,lcolG,revl),(win.adjustedRectX+30,win.adjustedRectY+30,32,48))
        pygame.draw.rect(screen,(lcolR,lcolG,revl),(win.adjustedRectX+30,win.adjustedRectY+90,32,48))
        pygame.draw.rect(screen,(rcolR,rcolG,revr),(win.adjustedRectX+90,win.adjustedRectY+30,32,48))
        pygame.draw.rect(screen,(rcolR,rcolG,revr),(win.adjustedRectX+90,win.adjustedRectY+90,32,48))

def displayBotConfig(screen,clock,win,events,cursor_rect):
    if win.active:
        ApplyButton.updatePos(win.adjustedRectX+100,win.adjustedRectY+155,70,24)
        CancelButton.updatePos(win.adjustedRectX+190,win.adjustedRectY+155,70,24)
        weaponConfig.updatePos(win.adjustedRectX+10,win.adjustedRectY+30,100,24)
        ApplyButton.active = True
        CancelButton.active = True
        weaponConfig.active = True
        weaponConfig.update(screen,cursor_rect,events)
        ApplyButton.update(screen,cursor_rect,events)
        CancelButton.update(screen,cursor_rect,events)
        if ApplyButton.clicked_up:
            win.active = False
        if CancelButton.clicked_up:
            win.active = False

def renderView(screen,cursor_img_rect,events):
    global viewOpen
    global showPhysics
    if viewOpen:
        pygame.draw.rect(screen,(16,16,16),(60,24,100,200))
        performanceButton.active = True
        performanceButton.update(screen,cursor_img_rect,events)
        positionsButton.active = True
        positionsButton.update(screen,cursor_img_rect,events)
        motorsButton.active = True
        motorsButton.update(screen,cursor_img_rect,events)
        botConfigButton.active = True
        botConfigButton.update(screen,cursor_img_rect,events)
        uiHandler.draw_text(screen,90,125,font_small,"Physics","#828282")
        showPhysicsButton.active = True
        showPhysicsButton.update(screen,cursor_img_rect,events)
        if "mouse_button_up" in events and not viewButton.clicked_up:
            viewOpen = False
            performanceButton.active = False
            positionsButton.active = False
            motorsButton.active = False
        if performanceButton.clicked_up and performanceWin.active:
            performanceWin.active = False
            performanceButton.text = "  Performance"
        elif performanceButton.clicked_up and not performanceWin.active:
            performanceWin.active = True
            performanceButton.text = "✓ Performance"
        if positionsButton.clicked_up and posWin.active:
            posWin.active = False
            positionsButton.text = "  Positions"
        elif positionsButton.clicked_up and not posWin.active:
            posWin.active = True
            positionsButton.text = "✓ Positions"
        if motorsButton.clicked_up and motorWin.active:
            motorWin.active = False
            motorsButton.text = "  Motors"
        elif motorsButton.clicked_up and not motorWin.active:
            motorWin.active = True
            motorsButton.text = "✓ Motors"
        if botConfigButton.clicked_up and botConfigWin.active:
            botConfigWin.active = False
            botConfigButton.text = "  Bot Config"
        elif botConfigButton.clicked_up and not botConfigWin.active:
            botConfigWin.active = True
            botConfigButton.text = "✓ Bot Config"
        if showPhysicsButton.clicked_up and not showPhysics:
            showPhysics = True
            showPhysicsButton.text = "✓ Show hitboxes"
        elif showPhysicsButton.clicked_up and showPhysics:
            showPhysics = False
            showPhysicsButton.text = "  Show hitboxes"

def renderTimer(screen,cursor_img_rect,events):
    global timerOpen
    global timerRunning
    global timerMode
    global timerStart_ticks
    if timerOpen:
        pygame.draw.rect(screen,(16,16,16),(140,24,100,200))
        compModeButton.active = True
        compModeButton.update(screen,cursor_img_rect,events)
        autonSkillsButton.active = True
        autonSkillsButton.update(screen,cursor_img_rect,events)
        driverSkillsButton.active = True
        driverSkillsButton.update(screen,cursor_img_rect,events)
        noTimerButton.active = True
        noTimerButton.update(screen,cursor_img_rect,events)
        uiHandler.draw_text(screen,190,132,font_small,"---Controls---","#878787")
        runTimerButton.active = True
        runTimerButton.update(screen,cursor_img_rect,events)
        if "mouse_button_up" in events and not timerButton.clicked_up:
            timerOpen = False
            compModeButton.active = False
            autonSkillsButton.active = False
            driverSkillsButton.active = False
            noTimerButton.active = False
            runTimerButton.active = False
        if compModeButton.clicked_up:
            compModeButton.text = "✓ Comp"
            autonSkillsButton.text = "  Skills: Auton"
            driverSkillsButton.text = "  Skills: Driver"
            noTimerButton.text = "  Stopwatch"
            timerMode = "comp"
        if autonSkillsButton.clicked_up:
            compModeButton.text = " Comp"
            autonSkillsButton.text = "✓ Skills: Auton"
            driverSkillsButton.text = "  Skills: Driver"
            noTimerButton.text = "  Stopwatch"
            timerMode = "sa"
        if driverSkillsButton.clicked_up:
            compModeButton.text = "  Comp"
            autonSkillsButton.text = "  Skills: Auton"
            driverSkillsButton.text = "✓ Skills: Driver"
            noTimerButton.text = "  Stopwatch"
            timerMode = "sd"
        if noTimerButton.clicked_up:
            compModeButton.text = "  Comp"
            autonSkillsButton.text = "  Skills: Auton"
            driverSkillsButton.text = "  Skills: Driver"
            noTimerButton.text = "✓ Stopwatch"
            timerMode = "disable"

while 1: # Main game loop
    # Get time, solve for FPS
    ticks = pygame.time.get_ticks()
    fps = clock.get_fps()
    try:
        fpsSpeedScale = fps/60
    except Exception:
        fpsSpeedScale = 10
        print("Warning: 0 FPS, temporarily scaling speed to 1")
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
    elif runTimerButton.clicked_up or "space_down" in events: 
        if timerRunning:
            timerStart_ticks = pygame.time.get_ticks()
            timerRunning = False
            runTimerButton.text = "Run timer (space)"
        else:
            timerRunning = True
            runTimerButton.text = "Stop timer (space)"
            if timerMode == "comp":
                totalSecondsRemaining = 180
                matchTime = 180
            if timerMode == "sa" or timerMode == "sd":
                totalSecondsRemaining = 60
                matchTime = 60
            if timerMode == "disabled":
                totalSecondsRemaining = -1
                matchTime = 1
    elif "powerUp" in events:
        addPwr = True
        if power <= 100:
            power += .05*fpsSpeedScale
    elif "powerDown" in events:
        addPwr = False
        if power >= 0:
            power -= .05*fpsSpeedScale
    elif "fire" in events:
        if botHeldDisks > 0:
            physicsHandler.fire(botHeldDisks,discX,discY,targetX,targetY,targetI,targetXInv,targetYInv,botX,botY,botDir,power,angle)
            botHeldDisks -=1
    try:
        if eventHandler.control.joy_name == "":
            recordBotKeystrokes(events)
        else:
            moveLeftSide = eventHandler.control.axis_data[1]*512/fpsSpeedScale
            moveRightSide = eventHandler.control.axis_data[3]*512/fpsSpeedScale
    except Exception:
        recordBotKeystrokes(events,fpsSpeedScale)

    if power <= 100 and addPwr:
        power += .05*fpsSpeedScale
    elif power >= 0 and not addPwr:
        power -= .025*fpsSpeedScale
    
    # Bot control simulation
    botDir += (moveLeftSide-moveRightSide)/256
    botRadians = math.radians(botDir-180)
    botX += -((moveLeftSide+moveRightSide)/256) * math.sin(botRadians)
    botY += -((moveLeftSide+moveRightSide)/256) * math.cos(botRadians)
    if botDir>360:
        botDir = 0
    elif botDir<0:
        botDir = 360
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
    screen.fill("#0f0f0f")
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
    # Get rects for collision
    botRect = pygame.Rect((botX,botY),(64,64))
    discX,discY,[botX,botY],botRadians = physicsHandler.updatePhysics(discX,discY,targetI,botRect.centerx,botRect.centery,botRadians,fps,screen,height,width,panOffsetX,panOffsetY,zoomScale,showPhysics) # Render box2d physics 
    botX -= 32
    botY -= 32
    botDir = math.degrees(botRadians)+180
    for i in range(len(discX)): # Check collision and draw, sees length instead of values to support multiple disks at same position 
        if i in targetI:
            targetxi = targetX[targetI.index(i)]
            targetyi = targetY[targetI.index(i)]
            targetXInvV = targetXInv[targetI.index(i)]
            targetYInvV = targetYInv[targetI.index(i)]
            addX = targetxi/targetyi
            addY = targetyi/targetxi
            try:
                if targetxi < discX[i]:
                    discX[i] += addX*10*fpsSpeedScale
                if targetyi < discY[i]:    
                    discY[i] += addY*10*fpsSpeedScale
                if targetxi > discX[i]:
                    discX[i] -= addX*10*fpsSpeedScale
                if targetyi > discY[i]:    
                    discY[i] -= addY*10*fpsSpeedScale
            except IndexError:
                print("disk animation error")
            try:
                if not targetXInvV and targetxi >= discX[i]:
                    targetX.pop(targetI.index(i))
                    targetY.pop(targetI.index(i))
                    targetI.pop(targetI.index(i))
                    targetXInv.pop(targetI.index(i))
                    targetYInv.pop(targetI.index(i))
                if targetXInvV and targetxi <= discX[i]:
                    targetX.pop(targetI.index(i))
                    targetY.pop(targetI.index(i))
                    targetI.pop(targetI.index(i))
                    targetXInv.pop(targetI.index(i))
                    targetYInv.pop(targetI.index(i))
                if not targetYInvV and targetyi >= discY[i]:
                    targetX.pop(targetI.index(i))
                    targetY.pop(targetI.index(i))
                    targetI.pop(targetI.index(i))
                    targetXInv.pop(targetI.index(i))
                    targetYInv.pop(targetI.index(i))
                if targetYInvV and targetyi <= discY[i]:
                    targetX.pop(targetI.index(i))
                    targetY.pop(targetI.index(i))
                    targetI.pop(targetI.index(i))
                    targetXInv.pop(targetI.index(i))
                    targetYInv.pop(targetI.index(i))
            except Exception:
                try:
                    targetX.pop(targetI.index(i))
                    targetY.pop(targetI.index(i))
                    targetI.pop(targetI.index(i))
                    targetXInv.pop(targetI.index(i))
                    targetYInv.pop(targetI.index(i))
                except Exception:
                    pass
                print("Probably reached target")
        try:
            screen.blit(scaledDisc,((discX[i]*zoomScale/100)+(width/2+panOffsetX),(discY[i]*zoomScale/100)+(height/2+panOffsetY)))    
        except Exception:
            print("Blit error")
        try:
            currentDiscRect = pygame.Rect((discX[i],discY[i]),(16,16))
            if currentDiscRect.colliderect(botRect) and botHeldDisks<3 and intake==True: 
                discX.pop(i)
                discY.pop(i)
                botHeldDisks +=1
        except IndexError:
            print("disk not in index")
            pass        
    # Draw bots before anything above it
    scaledRedBot = pygame.transform.scale(fileHandler.redbot,(32*(zoomScale/50),32*(zoomScale/50)))
    scaledRedBot = pygame.transform.rotate(scaledRedBot,botDir)
    screen.blit(scaledRedBot,((width/2+panOffsetX)+(botX*zoomScale/100),(height/2+panOffsetY)+(botY*zoomScale/100)))
    uiHandler.draw_text(screen,(width/2+panOffsetX)+((botX+32)*zoomScale/100),(height/2+panOffsetY)+((botY+32)*zoomScale/100),font_default,"%d"%botHeldDisks,"#FFFFFF")
    pygame.draw.rect(screen,(64,64,64),((550*zoomScale/100)+(width/2 + panOffsetX),(784*zoomScale/100)+(height/2+panOffsetY),(64*zoomScale/100),(16*zoomScale/100)))
    if ColorRoller1Custody == 0:
        pygame.draw.rect(screen,(255,0,0),((554*zoomScale/100)+(width/2 + panOffsetX),(784*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(16*zoomScale/100)))
        pygame.draw.rect(screen,(0,0,255),((554*zoomScale/100)+(width/2 + panOffsetX),(784*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(8*zoomScale/100)))
    if ColorRoller1Custody == 1:
        pygame.draw.rect(screen,(0,0,255),((554*zoomScale/100)+(width/2 + panOffsetX),(784*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(16*zoomScale/100)))
        pygame.draw.rect(screen,(255,0,0),((554*zoomScale/100)+(width/2 + panOffsetX),(784*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(8*zoomScale/100)))
    if ColorRoller1Custody == 2:
        pygame.draw.rect(screen,(0,0,255),((554*zoomScale/100)+(width/2 + panOffsetX),(784*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(16*zoomScale/100)))
    if ColorRoller1Custody == 3:
        pygame.draw.rect(screen,(255,0,0),((554*zoomScale/100)+(width/2 + panOffsetX),(784*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(16*zoomScale/100)))
    pygame.draw.rect(screen,(64,64,64),((200*zoomScale/100)+(width/2 + panOffsetX),(0*zoomScale/100)+(height/2+panOffsetY),(64*zoomScale/100),(16*zoomScale/100)))
    if ColorRoller2Custody == 0:
        pygame.draw.rect(screen,(255,0,0),((204*zoomScale/100)+(width/2 + panOffsetX),(0*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(16*zoomScale/100)))
        pygame.draw.rect(screen,(0,0,255),((204*zoomScale/100)+(width/2 + panOffsetX),(8*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(8*zoomScale/100)))
    if ColorRoller2Custody == 1:
        pygame.draw.rect(screen,(0,0,255),((204*zoomScale/100)+(width/2 + panOffsetX),(0*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(16*zoomScale/100)))
        pygame.draw.rect(screen,(255,0,0),((204*zoomScale/100)+(width/2 + panOffsetX),(8*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(8*zoomScale/100)))
    if ColorRoller2Custody == 2:
        pygame.draw.rect(screen,(0,0,255),((204*zoomScale/100)+(width/2 + panOffsetX),(0*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(16*zoomScale/100)))
    if ColorRoller2Custody == 3:
        pygame.draw.rect(screen,(255,0,0),((204*zoomScale/100)+(width/2 + panOffsetX),(0*zoomScale/100)+(height/2+panOffsetY),(48*zoomScale/100),(16*zoomScale/100)))
    pygame.draw.rect(screen,(64,64,64),((0*zoomScale/100)+(width/2 + panOffsetX),(150*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(64*zoomScale/100)))
    if ColorRoller3Custody == 0:
        pygame.draw.rect(screen,(255,0,0),((0*zoomScale/100)+(width/2 + panOffsetX),(154*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(48*zoomScale/100)))
        pygame.draw.rect(screen,(0,0,255),((8*zoomScale/100)+(width/2 + panOffsetX),(154*zoomScale/100)+(height/2+panOffsetY),(8*zoomScale/100),(48*zoomScale/100)))
    if ColorRoller3Custody == 1:
        pygame.draw.rect(screen,(0,0,255),((0*zoomScale/100)+(width/2 + panOffsetX),(154*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(48*zoomScale/100)))
        pygame.draw.rect(screen,(255,0,0),((8*zoomScale/100)+(width/2 + panOffsetX),(154*zoomScale/100)+(height/2+panOffsetY),(8*zoomScale/100),(48*zoomScale/100)))
    if ColorRoller3Custody == 2:
        pygame.draw.rect(screen,(0,0,255),((0*zoomScale/100)+(width/2 + panOffsetX),(154*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(48*zoomScale/100)))
    if ColorRoller3Custody == 3:
        pygame.draw.rect(screen,(255,0,0),((0*zoomScale/100)+(width/2 + panOffsetX),(154*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(48*zoomScale/100)))
    pygame.draw.rect(screen,(64,64,64),((782*zoomScale/100)+(width/2 + panOffsetX),(600*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(64*zoomScale/100)))
    if ColorRoller4Custody == 0:
        pygame.draw.rect(screen,(255,0,0),((782*zoomScale/100)+(width/2 + panOffsetX),(604*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(48*zoomScale/100)))
        pygame.draw.rect(screen,(0,0,255),((782*zoomScale/100)+(width/2 + panOffsetX),(604*zoomScale/100)+(height/2+panOffsetY),(8*zoomScale/100),(48*zoomScale/100)))
    if ColorRoller4Custody == 1:
        pygame.draw.rect(screen,(0,0,255),((782*zoomScale/100)+(width/2 + panOffsetX),(604*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(48*zoomScale/100)))
        pygame.draw.rect(screen,(255,0,0),((782*zoomScale/100)+(width/2 + panOffsetX),(604*zoomScale/100)+(height/2+panOffsetY),(8*zoomScale/100),(48*zoomScale/100)))
    if ColorRoller4Custody == 2:
        pygame.draw.rect(screen,(0,0,255),((782*zoomScale/100)+(width/2 + panOffsetX),(604*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(48*zoomScale/100)))
    if ColorRoller4Custody == 3:
        pygame.draw.rect(screen,(255,0,0),((782*zoomScale/100)+(width/2 + panOffsetX),(604*zoomScale/100)+(height/2+panOffsetY),(16*zoomScale/100),(48*zoomScale/100)))
    if colorRoller1Rect.colliderect(botRect) and intake and "user_event_2" in events:
        print("Color roller 1 changing")
        if ColorRoller1Custody == 0:
            ColorRoller1Custody = 2
        elif ColorRoller1Custody == 1:
            ColorRoller1Custody = 3
        elif ColorRoller1Custody == 2:
            ColorRoller1Custody = 1
        elif ColorRoller1Custody == 3:
            ColorRoller1Custody = 0
    if colorRoller2Rect.colliderect(botRect) and intake and "user_event_2" in events:
        print("Color roller 2 changing")
        if ColorRoller2Custody == 0:
            ColorRoller2Custody = 2
        elif ColorRoller2Custody == 1:
            ColorRoller2Custody = 3
        elif ColorRoller2Custody == 2:
            ColorRoller2Custody = 1
        elif ColorRoller2Custody == 3:
            ColorRoller2Custody = 0
    if colorRoller3Rect.colliderect(botRect) and intake and "user_event_2" in events:
        print("Color roller 2 changing")
        if ColorRoller3Custody == 0:
            ColorRoller3Custody = 2
        elif ColorRoller3Custody == 1:
            ColorRoller3Custody = 3
        elif ColorRoller3Custody == 2:
            ColorRoller3Custody = 1
        elif ColorRoller3Custody == 3:
            ColorRoller3Custody = 0
    if colorRoller4Rect.colliderect(botRect) and intake and "user_event_2" in events:
        print("Color roller 2 changing")
        if ColorRoller4Custody == 0:
            ColorRoller4Custody = 2
        elif ColorRoller4Custody == 1:
            ColorRoller4Custody = 3
        elif ColorRoller4Custody == 2:
            ColorRoller4Custody = 1
        elif ColorRoller4Custody == 3:
            ColorRoller4Custody = 0
    # High goals
    screen.blit(scaledRedHighGoal,((width/2+panOffsetX)+(scaledFieldRect.width-(160*zoomScale/100)),(height/2+panOffsetY)+(50*zoomScale/100)))
    screen.blit(scaledBlueHighGoal,((width/2+panOffsetX)+(50*zoomScale/100),(height/2+panOffsetY)+(scaledFieldRect.height-(160*zoomScale/100))))
    uiHandler.draw_text(screen,(width/2+panOffsetX)+(scaledFieldRect.width-(90*zoomScale/100)),(height/2+panOffsetY)+(114*zoomScale/100),font_default,"%d"%redHighGoalDisks,"#FFFFFF")
    uiHandler.draw_text(screen,(width/2+panOffsetX)+(114*zoomScale/100),(height/2+panOffsetY)+(scaledFieldRect.height-(90*zoomScale/100)),font_default,"%d"%blueHighGoalDisks,"#FFFFFF")
    # Draw top menu bar
    pygame.draw.rect(screen,(32,32,32),(0,0,width,24))
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
    # Update menu items
    if viewButton.clicked_down:
        viewOpen = True
    if timerButton.clicked_down:
        timerOpen = True
    # Draw menu items
    renderView(screen,cursor_img_rect,events)
    renderTimer(screen,cursor_img_rect,events)
    
    if timerRunning:
        if not timerMode == "disabled":
            if not totalSecondsRemaining == 0:
                totalSecondsRemaining = matchTime - math.floor((pygame.time.get_ticks()-timerStart_ticks)/1000)
            else:
                timerRunning = False
        elif timerMode == "disabled":
            totalSecondsRemaining = math.floor((pygame.time.get_ticks()-timerStart_ticks)/1000)

    uiHandler.draw_text(screen,width/2-20,10,font_small,str(bScore),"#0000ff")
    uiHandler.draw_text(screen,width/2,10,font_small,"|","#870087")
    uiHandler.draw_text(screen,width/2+20,10,font_small,str(rScore),"#ff0000")
    minutesRemaining = math.floor(totalSecondsRemaining/60)
    secondsRemaining = totalSecondsRemaining-(minutesRemaining*60)

    if timerMode == "comp":    
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
    elif timerMode == "sa":
        gameStageText = "End/AT"
        modeMinutesRemaining = minutesRemaining
        modeSecondsRemaining = secondsRemaining
    elif timerMode == "sd":
        gameStageText = "End/DC"
        modeMinutesRemaining = minutesRemaining
        modeSecondsRemaining = secondsRemaining
    else:
        gameStageText = "Inf/DC"
        modeMinutesRemaining = 99
        modeSecondsRemaining = 99

    if secondsRemaining>=10:
        addzero = ""
    else:
        addzero = "0"
    
    if modeSecondsRemaining>=10:
        addModeZero = ""
    else:
        addModeZero = "0"

    uiHandler.draw_text(screen,width-40,10,font_small,"Time: %d:%s%d"%(minutesRemaining,addzero,secondsRemaining),"#ffffff")
    uiHandler.draw_text(screen,width-110,10,font_small,"%s: %d:%s%d"%(gameStageText,modeMinutesRemaining,addModeZero,modeSecondsRemaining),"#ffffff")
    # Draw windows
    posWin.update(screen,cursor_img_rect,events)
    performanceWin.update(screen,cursor_img_rect,events)
    motorWin.update(screen,cursor_img_rect,events)
    botConfigWin.update(screen,cursor_img_rect,events)
    # Run window tasks
    displayPerformanceStats(screen,clock,performanceWin,events)
    displayPositionStats(screen,clock,posWin,events)
    displayMotorStats(screen,clock,motorWin,events,moveLeftSide,moveRightSide,power)
    displayBotConfig(screen,clock,botConfigWin,events,cursor_img_rect)

    # Objects to be rendered last so huds and displays can show overlays
    # Zoom overlay
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

    # Draw scale
    pygame.draw.rect(screen,"#ffffff",(32,height-32,physicsHandler.ppm*(zoomScale/100),5))
    pygame.draw.rect(screen,"#000000",(32,height-32,physicsHandler.ppm*(zoomScale/200),5))
    uiHandler.draw_text(screen,20,height-20,font_small,"m","#ffffff")
    uiHandler.draw_text(screen,32,height-20,font_small,"0","#ffffff")
    uiHandler.draw_text(screen,32+(physicsHandler.ppm*zoomScale/100),height-20,font_small,"1","#ffffff")
    uiHandler.draw_text(screen,20,height-40,font_small,"ft","#ffffff")
    uiHandler.draw_text(screen,32,height-40,font_small,"0","#ffffff")
    uiHandler.draw_text(screen,32+((physicsHandler.ppm/3.281)*(zoomScale/100)),height-40,font_small,"1","#ffffff")
    uiHandler.draw_text(screen,32+(((physicsHandler.ppm/3.281)*2)*(zoomScale/100)),height-40,font_small,"2","#ffffff")
    uiHandler.draw_text(screen,32+(((physicsHandler.ppm/3.281)*3)*(zoomScale/100)),height-40,font_small,"3","#ffffff")
    screen.blit(cursors[0], cursor_img_rect)
    pygame.display.flip()
    clock.tick(framelimit)


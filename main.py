# Pygame
import math
import pygame

# Custom modules
import eventHandler
import fileHandler
import uiHandler
import physicsHandler
import crashHandler

#Other
import psutil
import traceback

# Cores
import Cores.SpinUp.core as Core

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

pygame.display.set_caption("Spin Up - botemu")
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
ApplyButton = uiHandler.Button(font_small,70,24,80,24,1,text = "OK",box_color="#1f3f6f",text_color="#ffffff",active=False)

fileOpen = False
editOpen = False
viewOpen = False
gameOpen = False
aiOpen = False
timerOpen = False
recOpen = False

# Window definitions here
performanceWin = uiHandler.window(screen,"Performance",(25,100,200,200),True,False,"#0050cf",True)
posWin = uiHandler.window(screen,"Error - Positions",(25,300,200,100),True,False,"#870000",True)
motorWin = uiHandler.window(screen,"Motors",(25,450,200,150),True,False,"#870000",False)
botConfigWin = uiHandler.window(screen,"Error - Bot config",(250,250,200,100),True,False,"#870000",False)
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

def displayPositionStats(screen,clock,win,events,cursor_rect = cursor_img_rect):
    global botX
    global botY
    global botDir
    global power
    if win.active:
        try:
            Core.posWin.active = True
            Core.displayPositionStats(screen,clock,Core.posWin,events,font_small)
        except Exception:
            win.active = True
            uiHandler.draw_text(screen,win.adjustedRectX,win.adjustedRectY+24,font_small,"Error: This core doesn't have a position window","#FFFFFF")
            ApplyButton.updatePos(win.adjustedRectX+100,win.adjustedRectY+50,70,24)
            ApplyButton.active = True
            ApplyButton.update(screen,cursor_rect,events)
            if ApplyButton.clicked_up:
                win.active = False

def displayBotConfig(screen,clock,win,events,cursor_rect):
    if win.active:
        try:
            Core.botConfigWin.active = True
            Core.botConfig(screen,clock,Core.botConfigWin,events,font_small)
        except Exception:
            win.active = True
            uiHandler.draw_text(screen,win.adjustedRectX,win.adjustedRectY+24,font_small,"Error: This core doesn't have a bot config tool","#FFFFFF")
            ApplyButton.updatePos(win.adjustedRectX+100,win.adjustedRectY+50,70,24)
            ApplyButton.active = True
            ApplyButton.update(screen,cursor_rect,events)
            if ApplyButton.clicked_up:
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
Core.getScreen(screen)
try:
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
        
        # Run core
        Core.renderall(screen,width,height,panOffsetX,panOffsetY,zoomScale,fpsSpeedScale,events,font_default,fps,showPhysics)
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
        Core.displayMotorStats(screen,clock,motorWin,events)
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
        # a #Test crash handler with this
except Exception as exc:
    crashHandler.generateCrashMessage(''.join(traceback.format_exception(None, exc, exc.__traceback__)))
    print("Software crashed!\n======================================")
    traceback.print_exc()
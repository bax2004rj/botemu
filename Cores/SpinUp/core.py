# Botemu game rendering/example (2022/2023 Spin Up game)
import coreFileHandler
import pygame
import corePhysicsHandler
# Nab from main
import sys
from os import path
maindirectory = path.path(__file__).abspath()
sys.path.append(maindirectory.parent.parent)
import botemu.uiHandler

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

botConfigWin = uiHandler.window(screen,"Bot Configuration",(250,250,400,200),True,False,"#008250",False)

def liveScore(): # Calculate 
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
    return bScore,rScore
        

def renderLayer1(screen,width,height,panOffsetX,panOffsetY,zoomScale,fpsSpeedScale): # Render everything that appears under the bot
    scaledGameField = pygame.transform.scale(coreFileHandler.gameField,(playfieldRect.width*(zoomScale/100),playfieldRect.height*(zoomScale/100)))
    scaledDisc = pygame.transform.scale(coreFileHandler.disc,(playfieldRect.width*(zoomScale/100)*.05,playfieldRect.height*(zoomScale/100)*.05))
    scaledRedHighGoal = pygame.transform.scale(coreFileHandler.redHighGoal,(redHighGoalRect.width*(zoomScale/100)*.25,redHighGoalRect.height*(zoomScale/100)*.25))
    scaledBlueHighGoal = pygame.transform.scale(coreFileHandler.blueHighGoal,(blueHighGoalRect.width*(zoomScale/100)*.25,blueHighGoalRect.height*(zoomScale/100)*.25))
    scaledBlueLowGoal = pygame.transform.scale(coreFileHandler.blueLowGoal,(blueLowGoalRect.width*(zoomScale/100)*.275,blueHighGoalRect.height*(zoomScale/100)*.25))
    scaledRedLowGoal = pygame.transform.scale(coreFileHandler.redLowGoal,(blueLowGoalRect.width*(zoomScale/100)*.30,blueHighGoalRect.height*(zoomScale/100)*.25))
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
                physicsHandler.changediskdata()
                discX = physicsHandler.discX
                discY = physicsHandler.discY
                botHeldDisks +=1
        except IndexError:
            print("disk not in index")
            pass        

def renderLayer2(screen,width,height,panOffsetX,panOffsetY,zoomScale): # Render everything that appears above the bot
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
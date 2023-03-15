import math
import pygame
import Box2D
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

ppm = 221.22366237
discX = [100,200,300,400,500,600,700,460,356,290,155]
discY = [100,200,300,400,500,600,700,565,486,411,285]

def fire(botHeldDisks,discX,discY,targetX,targetY,targetI,targetXInv,targetYInv,botX,botY,botDir,power,angle): # Solve firing physics
    powerRange = ((power**2)*(math.sin(2*angle)))/-9.81
    botRadians = math.radians(botDir-180)
    discX.append(int(botX))
    discY.append(int(botY))
    targetX.append(botX+(powerRange/256) * math.sin(botRadians))
    targetY.append(botY+(powerRange/256) * math.cos(botRadians))
    targetI.append(len(discX))
    if targetX[-1] > botX:
        targetXInv.append(True)
    elif targetX[-1] < botX:
        targetXInv.append(False)
    if targetY[-1] > botY:
        targetYInv.append(True)
    elif targetY[-1] < botY:
        targetYInv.append(False)
    print("Range: %f,Target pos:(%d,%d)"%(powerRange,targetX[-1],targetY[-1]))

def testfire(power,angle,botx,boty,botDir,screen,zoom,panOffsetX,panOffsetY,color = "#cf3c00"):
    powerRange = ((power**2)*(math.sin(2*angle)))/-9.81
    botRadians = math.radians(botDir-180)
    targetDraw = []
    zoomAdjustedBotPos = [(botx+panOffsetX)*(zoom/100),(boty+panOffsetY)*(zoom/100)]
    targetOut = [botx+(powerRange/256) * math.sin(botRadians),boty+(powerRange/256) * math.cos(botRadians)]
    targetDraw.append((targetOut[0]+panOffsetX)*(zoom/100))
    targetDraw.append((targetOut[1]+panOffsetY)*(zoom/100))
    pygame.draw.line(screen,color,zoomAdjustedBotPos,targetOut,5)

world = world(gravity=(0, 0), doSleep=True)

# Walls
top_wall = world.CreateStaticBody(
    position=(0, 0),
    shapes=polygonShape(box=(3.5687, -0.032258)),
)
btm_wall = world.CreateStaticBody(
    position=(0, -3.5687),
    shapes=polygonShape(box=(3.5687, -0.032258)),
)
lef_wall = world.CreateStaticBody(
    position=(0, 0),
    shapes=polygonShape(box=(0.032258,-3.5687)),
)
rig_wall = world.CreateStaticBody(
    position=(3.5687, 0),
    shapes=polygonShape(box=(0.032258, -3.5687)),
)

# Low goal barriers
blg_x = world.CreateStaticBody(
    position=(2.65204, -1.25),
    shapes=polygonShape(box=(0.328803,-0.0508)),
)
blg_y = world.CreateStaticBody(
    position=(2.37204, -.95),
    shapes=polygonShape(box=(0.0508, -0.328803)),
)
rlg_x = world.CreateStaticBody(
    position=(0.9, -2.37204),
    shapes=polygonShape(box=(0.328803,-0.0508)),
)
rlg_y = world.CreateStaticBody(
    position=(1.214374, -2.75204),
    shapes=polygonShape(box=(0.0508, -0.328803)),
)

bot = world.CreateDynamicBody(position = (465/ppm,-730/ppm),angle = 0)
botPhysicRect = bot.CreatePolygonFixture(box = (0.125,0.125),density=1, friction=.3)

discPhysics = []
disks = []

# Temporary hitbox rendering system (likely removing when physics works for once), based on kne's demos
colors = {
    staticBody: (0, 255, 255, 127),
    dynamicBody: (127, 0, 255, 127),
}
def my_draw_polygon(polygon, body, fixture,SCREEN_HEIGHT,width,panOffsetx,panOffsetY,zoom,screen,PPM = 221.22366237):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [((v[0]*zoom/100)+(panOffsetx+(width/2)), SCREEN_HEIGHT/2+panOffsetY - v[1]*(zoom/100)) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)
polygonShape.draw = my_draw_polygon
def my_draw_circle(circle, body, fixture,SCREEN_HEIGHT,width,panOffsetx,panOffsetY,zoom,screen,PPM = 221.22366237):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
circleShape.draw = my_draw_circle

def changediskdata():
    global discX
    global discY
    global ppm
    global world
    global discPhysics
    global disks
    discPhysics = []
    disks = []
    for i in range(len(discX)):
        discPhysics.append(world.CreateDynamicBody(position = (discX[i]/ppm,-discY[i]/ppm)))
        disks.append(discPhysics[i].CreateCircleFixture(radius = 0.069977,density = 0.5,friction = 0.3))
changediskdata()

def updatePhysics(discX,discY,targetI,botx,boty,botdir,fps,screen,height,width,panOffsetx,panOffsetY,zoom,debug = False): # Create dynamic bodies for box2d
    global world
    global newdiscI
    global newdiscX
    global newdiscY
    body = []
    circle = []
    global bot
    bot.angle = botdir
    bot.position = [botx/ppm,-boty/ppm]
    # for i in range(len(discX)):# Eliminate any discs currently being animated
    #     if not i in targetI and i not in newdiscI:
    #         newdiscX.append(discX[i])
    #         newdiscY.append(discY[i])
    #         newdiscI.append(i)
    #     elif i in newdiscI:
    #         di = newdiscI.index(i)
    #         newdiscX[di]=discX[i]
    #         newdiscY[di]=discY[i]
    #     else: # Delete if criterion missed
    #         newdiscX.pop(i)
    #         newdiscY.pop(i)
    #         newdiscI.pop(i)
    #         world.DestroyBody(body[i])
    # for i in range(len(newdiscX)): # Check if object already there
    #     posX = newdiscX[i]/ppm
    #     posY = newdiscY[i]/ppm
    #     body.append(world.CreateDynamicBody(position=(posX,posY)))
    #     circle.append(body[-1].CreateCircleFixture(radius=0.07, density=1, friction=0.3))
    try:    
        world.Step(1/fps,10,10) # Give it time
    except ZeroDivisionError:
        world.Step(1,10,10)
    if debug:
        for body in world.bodies:
            for fixture in body.fixtures:
                fixture.shape.draw(body,fixture,height,width,panOffsetx,panOffsetY,zoom,screen)
    # Steal those positions back!
    # try:
    #     for i in newdiscI:
    #         discX[newdiscI.index(i)]=200
    #         discY[newdiscI.index(i)]=200
    # except IndexError:
    #     pass
    newBotPos = bot.position*ppm
    newBotPos[1] = -newBotPos[1]
    newBotRad = bot.angle
    return discX,discY,newBotPos,newBotRad



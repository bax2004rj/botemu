import math

import Box2D
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

ppm = 224.650948589
newdiscX = []
newdiscY = []
newdiscI = []

def fire(botHeldDisks,discX,discY,targetX,targetY,targetI,targetXInv,targetYInv,botX,botY,botDir,power,angle): # Solve firing physics
    if botHeldDisks>0:
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

world = world(gravity=(0, 0), doSleep=True)

ground_body = world.CreateStaticBody(
    position=(0, 0),
    shapes=polygonShape(box=(800, 800)),
)

def updatePhysics(discX,discY,targetI,botx,boty,botdir,fps): # Create dynamic bodies for box2d
    global world
    global newdiscI
    global newdiscX
    global newdiscY
    body = []
    circle = []
    bot = world.CreateDynamicBody(position = (botx/ppm,boty/ppm),angle = botdir)
    botPhysicRect = bot.CreatePolygonFixture(box = (0.5,0.5))
    for i in range(len(discX)):# Eliminate any discs currently being animated
        if not i in targetI and i not in newdiscI:
            newdiscX.append(discX[i])
            newdiscY.append(discY[i])
            newdiscI.append(i)
        elif i in newdiscI:
            di = newdiscI.index(i)
            newdiscX[di]=discX[i]
            newdiscY[di]=discY[i]
        else: # Delete if criterion missed
            newdiscX.pop(i)
            newdiscY.pop(i)
            newdiscI.pop(i)
            world.DestroyBody(body[i])
    for i in range(len(newdiscX)): # Check if object already there
        posX = newdiscX[i]/ppm
        posY = newdiscY[i]/ppm
        body.append(world.CreateDynamicBody(position=(posX,posY)))
        circle.append(body[-1].CreateCircleFixture(radius=0.07, density=1, friction=0.3))
    try:    
        world.Step(1/fps,10,10) # Give it time
    except ZeroDivisionError:
        world.Step(1,10,10)
    # Steal those positions back!
    try:
        for i in newdiscI:
            discX[newdiscI.index(i)]=200
            discY[newdiscI.index(i)]=200
    except IndexError:
        pass
    return discX,discY


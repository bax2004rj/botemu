import math
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


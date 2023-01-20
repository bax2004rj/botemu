# Pygame
import pygame
# Custom modules
import eventHandler
import uiHandler
import fileHandler

pygame.init()

width = 1000
height = 600
screen = pygame.display.set_mode((1000,600))

pygame.display.set_caption("5842C bot emulator")
pygame.mouse.set_visible(True)

clock = pygame.time.Clock()
# Font files here
font_default = fileHandler.get_font_default()
font_big = fileHandler.get_font_big()
font_small = fileHandler.get_font_small()

# Button definitions here
fileButton = uiHandler.Button(font_small,0,10,30,10,0,text="File")
editButton = uiHandler.Button(font_small,30,10,30,10,0,text="Edit")

get_ticks_last_frame = 0

bScore = 0
rScore = 0

while 1: # Main game loop
    uiHandler.draw_rectangle(screen,0,0,width,height,"#2f2f2f")
    ticks = pygame.time.get_ticks()
    delta_time = (ticks - get_ticks_last_frame) / 1000.0
    get_ticks_last_frame = ticks

    events = eventHandler.get_events()

    if "terminate" in events:
        pygame.quit()
        exit()
    screen.fill("#2f2f2f")
    uiHandler.draw_rectangle(screen,0,0,width,10,"#878787")
    fileButton.active = True
    editButton.active = True
    uiHandler.draw_text(screen,width/2-20,10,font_small,str(bScore),"#0000ff")
    uiHandler.draw_text(screen,width/2,10,font_small,"|","#870087")
    uiHandler.draw_text(screen,width/2+20,10,font_small,str(bScore),"#ff0000")
    pygame.display.flip()
    clock.tick(60)
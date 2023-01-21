# Pygame
import pygame
# Custom modules
import eventHandler
import uiHandler
import fileHandler

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

clock = pygame.time.Clock()
# Font files here
font_default = fileHandler.get_font_default()
font_big = fileHandler.get_font_big()
font_small = fileHandler.get_font_small()

minutesRemaining = 2
secondsRemaining = 59
modeMinutesRemaining = 0
modeSecondsRemaining = 15
recordMin = 0
recordSec = 00

zoomScale = 100
panOffsetX = 0
panOffsetY = 0

botX = 0
botY = 0
botDir = 0

# Button definitions here
fileButton = uiHandler.Button(font_small,30,24,0,0,1,text="File",button_type="procedural",active=True)
editButton = uiHandler.Button(font_small,30,24,30,0,1,text="Edit",button_type="procedural",active=True)
viewButton = uiHandler.Button(font_small,30,24,60,0,1,text="View",button_type="procedural",active=True)
gameButton = uiHandler.Button(font_small,30,24,90,0,1,text="Game",button_type="procedural",active=True)
aiButton = uiHandler.Button(font_small,20,24,120,0,1,text="AI",button_type="procedural",active=True)
timerButton = uiHandler.Button(font_small,35,24,140,0,1,text="Timer",button_type="procedural",active=True)
recButton = uiHandler.Button(font_small,50,24,width-200,0,1,text="REC: --:--",button_type="procedural",active=True,text_color="#ff0000")
get_ticks_last_frame = 0

bScore = 0
rScore = 0

autonTime = 15
driverControlTime = 165


while 1: # Main game loop
    # Get time, solve for FPS
    ticks = pygame.time.get_ticks()
    delta_time = (ticks - get_ticks_last_frame) / 1000.0
    get_ticks_last_frame = ticks
    # Check for window resize
    width,height = screen.get_size()
    # Move record button based on window size
    recButton.button_box_rect.topleft = width-220,0
    recButton.outline_rect.topleft = width-220.5,0

    # Check for events
    events = eventHandler.get_events()
    # Check if quitting
    if "terminate" in events:
        pygame.quit()
        exit()
    # Get mouse info for updates
    cursor_img_rect.topleft = pygame.mouse.get_pos()
    screen.fill("#2f2f2f")
    # Draw menus
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
    uiHandler.draw_text(screen,width-40,10,font_small,"Time: %d:%d"%(minutesRemaining,secondsRemaining),"#000000")
    uiHandler.draw_text(screen,width-110,10,font_small,"Auton: %d:%d"%(modeMinutesRemaining,modeSecondsRemaining),"#000000")
    screen.blit(cursors[0], cursor_img_rect)
    pygame.display.flip()
    clock.tick(60)


import pygame  # To load files
import json  # To save files
from json.decoder import JSONDecodeError  # For error handling
import os  # To find files

# Create directories
current_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(current_dir, 'bin')
font_dir = os.path.join(current_dir, 'Font')

audio_dir = os.path.join(current_dir, 'Audio')
music_dir = os.path.join(audio_dir, 'Music')
player_audio_dir = os.path.join(audio_dir, 'Player')
textures_dir = os.path.join(current_dir, 'Textures')
backgrounds_dir = os.path.join(textures_dir, 'Backgrounds')
game_dir = os.path.join(textures_dir, 'Game')

ui_dir = os.path.join(textures_dir, 'UI')

characters_dir = os.path.join(textures_dir, 'Character')
notes_dir = os.path.join(textures_dir, 'Notes')

other_textures_dir = os.path.join(textures_dir, 'Other')


music = os.path.join(audio_dir, 'Adventure_chiptune.mp3')
title_music = os.path.join(music_dir, 'title_menu.mp3')
gameover_music = os.path.join(music_dir, 'game_over.mp3')
shop_menu_music = os.path.join(music_dir, 'shop_menu.mp3')
sky_shop_music = os.path.join(music_dir, 'sky_shop.mp3')
char_shop_music = os.path.join(music_dir, 'char_shop.mp3')
level_music = os.path.join(music_dir, "level.mp3") 
pause_music = os.path.join(music_dir, "pause.mp3") 

# Load audio
pygame.mixer.init()
jump_sound = pygame.mixer.Sound(os.path.join(player_audio_dir, 'Jump.wav'))
game_over_sound = pygame.mixer.Sound(os.path.join(player_audio_dir, 'Game_over.wav'))
collect_sound = pygame.mixer.Sound(os.path.join(player_audio_dir, 'Collect.wav'))
hover_sound = pygame.mixer.Sound(os.path.join(audio_dir, 'Hover.wav'))
click_sound = pygame.mixer.Sound(os.path.join(audio_dir, 'Click.wav'))
pause_sound = pygame.mixer.Sound(os.path.join(audio_dir, 'Pause.wav'))

# Load images
# Misc. files:

cursor1 = pygame.image.load(os.path.join(ui_dir, 'defaultcursor.png'))
cursor2 = pygame.image.load(os.path.join(ui_dir, 'defaultcursor.png'))
cursor_files = [cursor1, cursor2]

pygame.font.init()
font_default = pygame.font.Font(os.path.join(font_dir, 'SourceSansPro-Regular.otf'), 25)
font_big = pygame.font.Font(os.path.join(font_dir, 'SourceSansPro-Regular.otf'), 50)
font_small = pygame.font.Font(os.path.join(font_dir, 'SourceSansPro-Regular.otf'), 14)

# Button files:
button_select = pygame.image.load(os.path.join(ui_dir, 'Button_select.png'))
button_hover = pygame.image.load(os.path.join(ui_dir, 'Button_hover.png'))
button = pygame.image.load(os.path.join(ui_dir, 'Button.png'))
button_states = [button_select, button_hover, button]

up_button = [pygame.image.load(os.path.join(ui_dir, 'Up.png')),
             pygame.image.load(os.path.join(ui_dir, 'Up_click.png'))]
right_button = [pygame.image.load(os.path.join(ui_dir, 'Right.png')),
                pygame.image.load(os.path.join(ui_dir, 'Right_click.png'))]
down_button = [pygame.image.load(os.path.join(ui_dir, 'Down.png')),
               pygame.image.load(os.path.join(ui_dir, 'Down_click.png'))]
left_button = [pygame.image.load(os.path.join(ui_dir, 'Left.png')),
               pygame.image.load(os.path.join(ui_dir, 'Left_click.png'))]
directional_buttons = [up_button, right_button, down_button, left_button]

# Pause button icons
pause_button = pygame.image.load(os.path.join(ui_dir, 'pause.png'))
pause_hover = pygame.image.load(os.path.join(ui_dir, 'pause_hover.png'))
pause_click = pygame.image.load(os.path.join(ui_dir, 'pause_click.png'))

# Vex game field parts
gameField = pygame.image.load(os.path.join(ui_dir, 'gameField.png'))
blueLowGoal = pygame.image.load(os.path.join(ui_dir, 'blueLowGoal.png'))
redLowGoal = pygame.image.load(os.path.join(ui_dir, 'redLowGoal.png'))
blueHighGoal = pygame.image.load(os.path.join(ui_dir, 'blueHighGoal.png'))
redHighGoal = pygame.image.load(os.path.join(ui_dir, 'redHighGoal.png'))
disc = pygame.image.load(os.path.join(ui_dir, 'disc.png'))
selectedDisc = pygame.image.load(os.path.join(ui_dir, 'selectedDisc.png'))


# Create functions so these files are accessible
def save_data(data):
    with open(os.path.join(save_dir, 's.bin'), 'w') as save_file:
        json.dump(data, save_file)


def get_save_data(data_layout):
    try:
        with open(os.path.join(save_dir, 's.bin')) as save_file:
            print("attempting to load file...")
            return json.load(save_file)
    except JSONDecodeError:
        print("JSON can't decode...")
        with open(os.path.join(save_dir, 's.bin'), 'w') as save_file_2:
            json.dump(data_layout, save_file_2)
        return data_layout
    except FileNotFoundError:
        print("file not found...")
        with open(os.path.join(save_dir, 's.bin'), 'w') as save_file_3:
            json.dump(data_layout, save_file_3)
        return data_layout



def get_font_default():
    return font_default


def get_font_big():
    return font_big


def get_font_small():
    return font_small


def get_music():
    return music


def get_jump_sound():
    return jump_sound


def get_game_over_sound():
    return game_over_sound


def get_collect_sound():
    return collect_sound


def get_hover_sound():
    return hover_sound


def get_click_sound():
    return click_sound


def get_pause_sound():
    return pause_sound


def get_directional_buttons():
    return directional_buttons


def get_button_states():
    return button_states


def get_title_music():
    return title_music

def get_gameover_music():
    return gameover_music

def get_shop_music():
    return shop_menu_music

def get_sky_music():
    return sky_shop_music

def get_char_music():
    return char_shop_music

def get_play_music():
    return level_music

def get_pause_music():
    return pause_music

def get_cursor_files():
    return cursor_files
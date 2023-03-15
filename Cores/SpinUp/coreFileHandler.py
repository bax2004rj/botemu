import pygame
import os
game_dir = os.path.join(os.getcwd(),"Assets")
# Core assets (When creating your own cores, you can replace these entirely with your own)
gameField = pygame.image.load(os.path.join(game_dir, 'gameField.png'))
blueLowGoal = pygame.image.load(os.path.join(game_dir, 'blueLowGoal.png'))
redLowGoal = pygame.image.load(os.path.join(game_dir, 'redLowGoal.png'))
blueHighGoal = pygame.image.load(os.path.join(game_dir, 'blueHighGoal.png'))
redHighGoal = pygame.image.load(os.path.join(game_dir, 'redHighGoal.png'))
disc = pygame.image.load(os.path.join(game_dir, 'disc.png'))
selectedDisc = pygame.image.load(os.path.join(game_dir, 'selectedDisc.png'))
bluebot = pygame.image.load(os.path.join(game_dir, 'bluebot.png'))
redbot = pygame.image.load(os.path.join(game_dir, 'redbot.png'))
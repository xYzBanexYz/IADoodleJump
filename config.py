import pygame
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('config')


try:
  pygame.init()
except:
  logger.error("Erreur initialisation pygame...")
  pygame.quit()
  quit()

#global variables
WINDOW_SIZE = (480,720)

# Jeff.py
PADDING = 20

# Player.py
SPEED = 7
JUMP_HEIGHT = 12
GRAVITY = 0.25
FRICTION = -0.10

#pygame stuff
clock = pygame.time.Clock()
display = pygame.display.set_mode(WINDOW_SIZE)
icon = pygame.image.load("./content/images/jeff.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption('Jeff Jump')

def quitGame():
  pygame.quit()
  logger.info("Jeu quitté.")
  sys.exit()
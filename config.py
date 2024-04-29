import pygame
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('config')
class config:
  def __init__(self, w=480, h=720):
    
    self.w = w
    self.h = h

    # Initialisation fenetre 
    try:
      pygame.init()
    except:
      logger.error("Erreur initialisation pygame...")
      pygame.quit()
      quit()

    self.display = pygame.display.set_mode((self.w, self.h))
    
    
    icon = pygame.image.load("./content/images/jeff.png").convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Jeff Jump')

    logger.info("Fenêtre lancée.")

    self.clock = pygame.time.Clock()

def quitGame():
  pygame.quit()
  logger.info("Jeu quitté.")
  sys.exit()
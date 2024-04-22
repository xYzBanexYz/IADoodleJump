import pygame
import logging
from enum import Enum

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('game')

try:
  pygame.init()
except:
  logger.error("Error initiating pygame...")
  pygame.quit()
  quit()

font = pygame.font.Font("./fonts/PixelifySansSemiBold.ttf", 20)

SPEED = 5

class DoodleGame:

  def __init__(self, w=480, h=720):
    self.w = w
    self.h = h
    # Initialisation fenetre 
    self.display = pygame.display.set_mode((self.w, self.h))
    logger.info("Fenêtre lancée.")

    pygame.display.set_caption('Doodle Jump')
    self.clock = pygame.time.Clock()
    # self.background = pygame.image.load("./images/background.png").convert()
    self.background = pygame.image.load("./images/back.png").convert()
    self.score = 0
    self.direction = Direction.STATIC

    player_img = pygame.image.load("./images/jeff_jumper.png")
    self.player_img = pygame.transform.scale(player_img, (player_img.get_width() * 1/4, player_img.get_height() * 1/4 ))  # Définis la taille souhaitée
    self.player_rect = self.player_img.get_rect(midbottom=(self.w // 2, 2*self.h // 3))

  def play_step(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          self.quit()
          quit() # TODO : Remplacer par menu
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        self.direction = Direction.LEFT
    elif keys[pygame.K_RIGHT]:
        self.direction = Direction.RIGHT
    else:
        self.direction = Direction.STATIC

    self._move()
    self._updateUI()
    self.clock.tick(60)
    #TODO

  def _updateUI(self):
    self.display.blit(self.background, (0,0))

    text = font.render(f"Score: {self.score}", False, "BLACK")
    self.display.blit(text, [5, 5])

    self.display.blit(self.player_img, self.player_rect)

    pygame.display.update()

  def quit(self):
    pygame.quit()
    logger.info("Jeu quitté.")
  
  def _move(self):
    match self.direction:
      case Direction.LEFT:
        self.player_rect.x -= SPEED
      case Direction.RIGHT:
        self.player_rect.x += SPEED
      case Direction.STATIC:
        pass
    
    self.player_rect.x = max(0, min(self.w - self.player_rect.width, self.player_rect.x))

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    STATIC = 3
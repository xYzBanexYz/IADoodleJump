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
  # Initialisation du jeu
  def __init__(self, w=480, h=720):
    self.w = w
    self.h = h
    self.on_menu = True
    self.on_play = False
    self.on_gameover = False
    self.playMusic = False

    # Initialisation fenetre 
    self.display = pygame.display.set_mode((self.w, self.h))
    
    pygame.display.set_caption('Jeff Jump')
    icon = pygame.image.load("./content/images/jeff.png").convert_alpha()
    pygame.display.set_icon(icon)
    logger.info("Fenêtre lancée.")

    self.clock = pygame.time.Clock()
    self.run = True
    self._intro()

  def _intro(self):
    pygame.mouse.set_visible(False)
    pro_max = pygame.image.load("./content/images/pro_max_plus.png").convert_alpha()
    pro_max_rect = pro_max.get_rect(center=(self.w//2, self.h//2))
    
    pygame.mixer.music.load("./content/sounds/effects/intro.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=0) 
    timer = 4000
    start_time = pygame.time.get_ticks()

    while timer > 0:
      self.display.fill((0,0,0))
      self.display.blit(pro_max, pro_max_rect)

      timer = max(0, 4000 - (pygame.time.get_ticks() - start_time))
      pygame.display.flip()
      self.clock.tick(60)

    pygame.mouse.set_visible(True) 
      



  # Menu
  def play_menu(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          self._quit()
          quit() # TODO : Remplacer par menu

    self.menu_background = pygame.image.load("./content/images/Menu/menu_background.jpg").convert()
    jeff_menu = pygame.image.load("./content/images/Menu/menu_image.png").convert_alpha()
    self.jeff_menu = pygame.transform.scale(jeff_menu, (jeff_menu.get_width() * 0.65, jeff_menu.get_height()*0.65)).convert_alpha()  # Définis la taille souhaitée
    self.jeff_menu_rect = self.jeff_menu.get_rect(center=(self.w//2, self.h//2 - 150))

    start_image = pygame.image.load("./content/images/Menu/start_btn.png")
    self.start_btn = Button(self.w // 2, self.h //2 + 80, start_image,0.9)

    exit_image = pygame.image.load("./content/images/Menu/exit_btn.png")
    self.exit_btn = Button(self.w // 2, self.h //2 + 230 , exit_image,0.9)

    self._updateMenuUI()

    if self.start_btn.click():
      self.on_play = True
      self._initGame()
      self._flushMenu()
      self.on_menu = False

    elif self.exit_btn.click():
      self._quit()       

    self.clock.tick(60)

  def _updateMenuUI(self):
    self.display.blit(self.menu_background, (0,0))
    self.display.blit(self.jeff_menu, self.jeff_menu_rect)

    self.start_btn.afficher(self.display)
    self.exit_btn.afficher(self.display)

    pygame.display.update()
  

  def _flushMenu(self):
    pygame.mixer.music.stop()
    self.menu_background = None
    self.jeff_menu = None
    self.jeff_menu_rect = None
    self.start_btn = None
    self.exit_btn = None
  
  def musicMenu(self):
    if (self.get_menu and not self.playMusic):
      pygame.mixer.music.load("./content/sounds/music/monaco.mp3")
      pygame.mixer.music.set_volume(0.5)
      pygame.mixer.music.play(loops=-1) 
      self.playMusic = True
    

  # Jeu 
  def _initGame(self):
    self.on_menu = False
    self.on_play = True
    self.on_gameover = False

    self.background = pygame.image.load("./content/images/Game/back.png").convert()
    self.score = 0
    self.direction = Direction.STATIC

    player_img = pygame.image.load("./content/images/Game/jeff_jumper.png")
    self.player_img = pygame.transform.scale(player_img, (player_img.get_width() * 1/4, player_img.get_height() * 1/4 ))  # Définis la taille souhaitée
    self.player_rect = self.player_img.get_rect(midbottom=(self.w // 2, 2*self.h // 3))

  def play_step(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          self._quit()
          quit()
    
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
  
  def _move(self):
    match self.direction:
      case Direction.LEFT:
        self.player_rect.x -= SPEED
      case Direction.RIGHT:
        self.player_rect.x += SPEED
      case Direction.STATIC:
        pass
    
    self.player_rect.x = max(0, min(self.w - self.player_rect.width, self.player_rect.x))

  def _updateUI(self):
    self.display.blit(self.background, (0,0))

    text = font.render(f"Score: {self.score}", False, "BLACK")
    self.display.blit(text, [5, 5])

    self.display.blit(self.player_img, self.player_rect)

    pygame.display.update()
  
  # Game over
  def _gameover(self):
    pass
    # TODO


  # Misc.
  def _quit(self):
    self.run = False
    pygame.quit()
    logger.info("Jeu quitté.")

  def _resetGame(self):
    self.background = None
    self.background = None
    self.score = 0
    self.direction = Direction.STATIC

    self.player_img = None
    self.player_rect = None

  # Getters
  def get_menu(self):
     return self.on_menu
  
  def get_play(self):
     return self.on_play
  
  def get_game_over(self):
     return self.on_gameover
  
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    STATIC = 3


class Button():
    def __init__(self, x, y, image, scale):
      width = image.get_width()
      height = image.get_height()
      self.base_image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
      self.image = self.base_image
      self.rect = self.image.get_rect()
      self.rect.center = (x, y)
      self.clicked = False
     
    def click(self):
      click = False
      pos = pygame.mouse.get_pos()

      if self.rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
          self.clicked = True
          click = True

      if pygame.mouse.get_pressed()[0] == 0:
        self.clicked = False
      return click
    
    def afficher(self, surface):
      surface.blit(self.image, (self.rect.x, self.rect.y))


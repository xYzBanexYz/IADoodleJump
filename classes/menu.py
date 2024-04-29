import pygame
import sys

from classes.button import Button

class Menu():
  def __init__(self, windowSize, screen, clock):
    self.start = False
    self.screen = screen
    self.clock = clock
    self.w, self.h = windowSize

    self.playMusic = False
    self.menu_background = pygame.image.load("./content/images/Menu/menu_background.jpg").convert()
    jeff_menu = pygame.image.load("./content/images/Menu/menu_image.png").convert_alpha()
    self.jeff_menu = pygame.transform.scale(jeff_menu, (jeff_menu.get_width() * 0.65, jeff_menu.get_height()*0.65)).convert_alpha()  # Définis la taille souhaitée
    self.jeff_menu_rect = self.jeff_menu.get_rect(center=(self.w//2, self.h//2 - 150))

    start_image = pygame.image.load("./content/images/Menu/start_btn.png")
    self.start_btn = Button(self.w // 2, self.h //2 + 80, start_image,0.9)

    exit_image = pygame.image.load("./content/images/Menu/exit_btn.png")
    self.exit_btn = Button(self.w // 2, self.h //2 + 230 , exit_image,0.9)

    self._launchMusic()

  def update(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          self._quit()

    self._updateMenuUI()

    if self.start_btn.click():
      self.start = True
      self._stopMusic()

    elif self.exit_btn.click():
      self._quit()       

    self.clock.tick(60)

  def _updateMenuUI(self):
    self.screen.blit(self.menu_background, (0,0))
    self.screen.blit(self.jeff_menu, self.jeff_menu_rect)

    self.start_btn.draw(self.screen)
    self.exit_btn.draw(self.screen)

    pygame.display.update()

  def _launchMusic(self):
    if not self.playMusic:
      pygame.mixer.music.load("./content/sounds/music/monaco.mp3")
      pygame.mixer.music.set_volume(0.5)
      pygame.mixer.music.play(loops=-1) 
      self.playMusic = True

  def _stopMusic(self):
    pygame.mixer.music.stop()
    self.playMusic = False
    
  def _quit(self):
    pygame.quit()
    sys.exit()

  def reset(self):
    pygame.mixer.music.stop()
    self.menu_background = None
    self.jeff_menu = None
    self.jeff_menu_rect = None
    self.start_btn = None
    self.exit_btn = None
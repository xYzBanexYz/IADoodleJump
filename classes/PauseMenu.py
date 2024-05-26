import pygame

from classes.button import Button
from config import quitGame, display, WINDOW_SIZE

class PauseMenu:

  def __init__(self):
    resume_image = pygame.image.load("./content/images/Pause/resume_btn.png").convert_alpha()
    self.resume_btn = Button(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] //2 + 20, resume_image,0.9)

    menu_image = pygame.image.load("./content/images/Pause/menu_btn.png").convert_alpha()
    self.menu_btn = Button(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] //2 + 180 , menu_image,0.9)

    self.background = pygame.image.load("./content/images/Pause/background.png").convert()

    self.jeff = pygame.image.load("./content/images/Pause/jeff.png").convert_alpha()
    self.jeffRect = self.jeff.get_rect(center= (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 200)) 


  def update(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quitGame()
      elif event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_ESCAPE:
          return "play"
    
    self._updateUI()

    if self.resume_btn.click():
      return "play"

    if self.menu_btn.click():
      return "menu"
    
    return ""
  
  def _updateUI(self):
    display.blit(self.background, (0,0))
    display.blit(self.jeff, self.jeffRect)

    self.resume_btn.draw(display)
    self.menu_btn.draw(display)

    pygame.display.update()
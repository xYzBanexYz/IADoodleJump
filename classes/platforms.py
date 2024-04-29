import pygame

from config import quitGame

class Platforms(pygame.sprite.Sprite):

  def __init__(self, platformType, x, y, windowSize):
    super().__init__()
    self.windowSize = windowSize
    match platformType:
      case "frite":
        self.image=  pygame.image.load("./content/images/Game/frite.png").convert_alpha()
      case "nevada":
        self.image = pygame.image.load("./content/images/Game/nevada.png").convert_alpha()

      case _:
        print("Invalid platform type.\nQuitting game...")
        quitGame()
    
    self.x, self.y = x, y
    self.rect = self.image.get_rect(midbottom=(self.x,self.y))

  def update(self, dy):
    self.y += dy
    
    if self.rect.y > self.windowSize[1]:
      self.kill()

  
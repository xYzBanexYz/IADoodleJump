import pygame

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
      """
      Checks if the button is clicked.

      Returns:
        bool: True if the button is clicked, False otherwise.
      """
      click = False
      pos = pygame.mouse.get_pos()

      if self.rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
          self.clicked = True
          click = True

      if pygame.mouse.get_pressed()[0] == 0:
        self.clicked = False
      return click
  
    def draw(self, surface):
      surface.blit(self.image, (self.rect.x, self.rect.y))
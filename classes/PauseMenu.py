import pygame

from classes.button import Button

class PauseMenu:

  def __init__(self, windowSize, screen, clock):
    self.display = screen
    self.clock = clock
    self.w, self.h = windowSize[0], windowSize[1]

    resume_image = pygame.image.load("./content/images/Pause/resume_btn.png")
    self.resume_btn = Button(self.w // 2, self.h //2 - 80, resume_image,0.9)

    exit_image = pygame.image.load("./content/images/Pause/exit_btn.png")
    self.restart_btn = Button(self.w // 2, self.h //2 + 80 , exit_image,0.9)

  def update(self):

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      elif event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_ESCAPE:
          return "play"
    
    self._updateUI()

    if self.resume_btn.click():
      return "play"


    return ""
  
  def _updateUI(self):
    self.display.fill((0,0,0))
    
    self.resume_btn.draw(self.display)
    self.restart_btn.draw(self.display)

    pygame.display.update()
import pygame

from classes.button import Button
from config import WINDOW_SIZE, clock, quitGame, display

class Menu():
  """Represents the main menu of the game."""

  def __init__(self):
    self.start = False
    self.playMusic = False
    self.menu_background = pygame.image.load("./content/images/Menu/menu_background.jpg").convert()

    jeff_menu = pygame.image.load("./content/images/Menu/menu_image.png").convert_alpha()
    self.jeff_menu = pygame.transform.scale(jeff_menu, (jeff_menu.get_width() * 0.65, jeff_menu.get_height()*0.65)).convert_alpha()
    self.jeff_menu_rect = self.jeff_menu.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 150))

    start_image = pygame.image.load("./content/images/Menu/start_btn.png")
    self.start_btn = Button(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] //2 + 80, start_image,0.9)

    exit_image = pygame.image.load("./content/images/Menu/exit_btn.png")
    self.exit_btn = Button(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] //2 + 230 , exit_image,0.9)

    # launching the famous "Ohhh Monaco! Chez toi il fait toujours beau!" music
    if not self.playMusic:
      pygame.mixer.music.stop()
      pygame.mixer.music.load("./content/sounds/music/monaco.mp3")
      pygame.mixer.music.set_volume(0.5)
      pygame.mixer.music.play(loops=-1) 
      self.playMusic = True

  def update(self):
    """Updates the menu and handles user input.

    Returns:
      str: The action to perform based on user input. Can be "play" or "exit".
    """
    if not self.playMusic:
      pygame.mixer.music.load("./content/sounds/music/monaco.mp3")
      pygame.mixer.music.set_volume(0.5)
      pygame.mixer.music.play(loops=-1) 
      self.playMusic = True

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quitGame()

    self._updateMenuUI()

    if self.start_btn.click():
      pygame.mixer.music.stop()
      self.playMusic = False
      return "play"
    
    elif self.exit_btn.click():
      quitGame()
      return "exit"       

    clock.tick(60)

  def _updateMenuUI(self):
    """Updates the menu user interface."""
    display.blit(self.menu_background, (0,0))
    display.blit(self.jeff_menu, self.jeff_menu_rect)

    self.start_btn.draw(display)
    self.exit_btn.draw(display)

    pygame.display.update()
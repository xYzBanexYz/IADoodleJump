import pygame
import os
import random

from config import quitGame
from entities.player import Player
from classes.platforms import Platforms

pygame.font.init()
font = pygame.font.Font("./content/fonts/PixelifySansSemiBold.ttf", 20)

PLAT_TYPE = ["frite", "nevada"]
SCROLL_SPEED = 5

class JeffGame:
  # Initialisation du jeu
  def __init__(self, windowSize, screen, clock):
    self.pause = False
    self.windowSize = windowSize
    self.restart = False
    self.display = screen
    self.clock = clock


    self.player = pygame.sprite.GroupSingle()
    self.player.add(Player(windowSize))

    self.platforms_group = pygame.sprite.Group()
    self.platforms_group.add(Platforms("frite", 240, 680, windowSize))

    self.background = pygame.image.load("./content/images/Game/back.png").convert()
    self.score = 0

  def play_step(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          quitGame()

    self._updateUI()
    self._checkCollisions()

    self.player.update(self._checkCollisions())
    # self.climb()



    self.clock.tick(60)

  def _updateUI(self):
    self.display.blit(self.background, (0,0))

    text = font.render(f"Score: {self.score}", False, "BLACK")
    self.display.blit(text, [5, 5])

    self.player.draw(self.display)
    self.platforms_group.draw(self.display)
    pygame.display.update()
  
  # Game over
  def _gameover(self):
    pass
    # TODO

  def _checkCollisions(self):
    if pygame.sprite.spritecollide(self.player.sprite, self.platforms_group, False): 
      return True
    else: return False

  def climb(self):
    if self.player.sprite.rect.y < self.windowSize[1] // 2:
        dy = self.windowSize[1] // 2 - self.player.sprite.rect.y
        
        for platform in self.platforms_group:
            platform.rect.y += dy
            
            if platform.rect.top > self.windowSize[1]:
                self.platforms_group.remove(platform)
                self.genPlatforms()
        self.score += dy


  def genPlatforms(self, x=0, y=0):
    if len(self.platforms_group) < 3:  
        if x == 0 and y == 0:
            x, y = random.randint(0, self.windowSize[0]), random.randint(0, self.windowSize[1] // 4)

        index = lambda: 0 if random.random() < 0.75 else 1
        ind = index()
        self.platforms_group.add(Platforms(PLAT_TYPE[ind], x, y, self.windowSize))

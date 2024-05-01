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

    self.firstPos = (random.randrange(50, windowSize[0]- 50), random.randrange(windowSize[1] // 2, windowSize[1]-50))
    self.player.add(Player(self.windowSize, *(self.firstPos)))

    self.platformsGroup = pygame.sprite.Group()
    self.platformsGroup.add(Platforms("frite", *(self.firstPos), windowSize))
    self.initializePlatforms()

    self.background = pygame.image.load("./content/images/Game/back.png").convert()
    self.score = 1



  def play_step(self):

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          quitGame()
      elif event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_ESCAPE:
          self.pause =  True
    

    self._updateUI()
    self._checkCollisions()

    self.player.update(self._checkCollisions())
    self.genPlatforms(self.player.sprite.rect.y)


    self.climb()

    self.clock.tick(60)

  def _updateUI(self):
    self.display.blit(self.background, (0,0))

    text = font.render(f"Score: {self.score}", False, "BLACK")
    self.display.blit(text, [5, 5])

    self.player.draw(self.display)
    self.platformsGroup.draw(self.display)
    pygame.display.update()
  
  # Game over
  def _gameover(self):
    pass
    # TODO

  def _checkCollisions(self):
    player_sprite = self.player.sprite
    collision_sprite = pygame.sprite.spritecollideany(player_sprite, self.platformsGroup)
    if collision_sprite:
        if player_sprite.rect.bottom <= collision_sprite.rect.centery:
            return True
    return False

  def climb(self):
    if self.player.sprite.rect.top < self.windowSize[1] // 4:
      self.player.sprite.pos.y += abs(self.player.sprite.vel.y)
      
      for platform in self.platformsGroup:
          platform.rect.y += abs(self.player.sprite.vel.y)
          
          if platform.rect.top > self.windowSize[1]:
              self.platformsGroup.remove(platform)
              platform.kill()
              self.score += 10

  def initializePlatforms(self):
     for _ in range(5):
        x, y = random.randint(50, self.windowSize[0]-50), random.randint(0, self.firstPos[1])

        index = lambda: 0 if random.random() < 0.75 else 1
        self.platformsGroup.add(Platforms(PLAT_TYPE[index()], x, y, self.windowSize))

  def genPlatforms(self, player_y):
    while len(self.platformsGroup) < 7:
        x, y = random.randint(50, self.windowSize[0]-50), random.randint(-(self.windowSize[1] // 2), 0)
        
        platform_accessible = any(abs(platform.rect.y - player_y) < 150 for platform in self.platformsGroup)
        
        if platform_accessible:
            index = lambda: 0 if random.random() < 0.75 else 1
            self.platformsGroup.add(Platforms(PLAT_TYPE[index()], x, y, self.windowSize))
        else:
            # Ajouter une plateforme de secours à une position accessible
            self.platformsGroup.add(Platforms(PLAT_TYPE[0], random.randint(50, self.windowSize[0]-50), player_y + 150, self.windowSize))
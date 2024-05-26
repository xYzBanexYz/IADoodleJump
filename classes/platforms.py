import pygame
from random import randint

from config import WINDOW_SIZE, SPEED
from entities.spring import Spring
class Platforms(pygame.sprite.Sprite):

  def __init__(self, x, y):
    super().__init__()
    self.image = pygame.image.load("./content/images/Game/frite.png").convert_alpha()
    self.rect = self.image.get_rect(midtop=(x + randint(-45, 45), y))
    rnd = randint(0,100)
    if rnd > 70:
      self.spring =  Spring(x,y)
    else:
      self.spring = None

class Nevada(Platforms):
  def __init__(self, x, y):
    super().__init__(x, y)
    self.crashed = False
    self.image = pygame.image.load("./content/images/Game/nevada.png").convert_alpha()
    self.rect = self.image.get_rect(center=(x, y))
    self.spring = None

  def crash(self):
    self.image = pygame.image.load("./content/images/Game/brokenNevada.png").convert_alpha()
    self.crashed = True

  def move(self):
    self.rect.y += SPEED // 2

class MovingFrite(Platforms):
  def __init__(self, x, y):
    super().__init__(x, y)
    self.dir = 1
    self.speed= randint(3, 5)

  def move(self):
    self.rect.x += self.dir * self.speed

    if self.rect.left <= 10 or self.rect.right >= WINDOW_SIZE[0] -10:
      self.dir = -self.dir
    if self.spring != None:
      self.spring.rect.x = self.rect.x

  
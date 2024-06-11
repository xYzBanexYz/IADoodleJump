import pygame
from random import randint

from config import WINDOW_SIZE, SPEED
from entities.spring import Spring
from entities.sauce import Sauce
class Platforms(pygame.sprite.Sprite):
  """Represents a platform in the game."""

  def __init__(self, x, y):
    """
    Initializes a new instance of the Platforms class.

    Args:
      x (int): The x-coordinate of the platform.
      y (int): The y-coordinate of the platform.
    """
    super().__init__()
    self.image = pygame.image.load("./content/images/Game/frite.png").convert_alpha()
    self.rect = self.image.get_rect(midtop=(x, y))
    rnd = randint(0, 100)
    if rnd > 70:
      self.spring = Spring(x + randint(-45, 45), y)
    else:
      self.spring = None
    rnd = randint(0, 100)
    if rnd > 90 and not self.spring:
      self.sauce = Sauce(x + randint(-45, 45), y)
    else:
      self.sauce = None
    

class Nevada(Platforms):
  def __init__(self, x, y):
    super().__init__(x, y)
    self.crashed = False
    self.image = pygame.image.load("./content/images/Game/nevada.png").convert_alpha()
    self.rect = self.image.get_rect(center=(x, y))
    self.spring = None
    self.sauce = None

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
    if self.sauce != None:
      self.sauce.rect.x = self.rect.x
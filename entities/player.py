import pygame
import os
from enum import Enum

SPEED = 5
JUMP_HEIGHT = 18
GRAVITY = 0.6

class Player(pygame.sprite.Sprite):

  def __init__(self, windowSize):
    super().__init__()

    self.jumping = False
    self.jump_height = JUMP_HEIGHT
    self.velocity = self.jump_height
    self.gravity = GRAVITY
    self.score = 0


    jeffStand =  pygame.image.load("./content/images/Game/jeff_jumper_up.png").convert_alpha()
    jeffJumping =  pygame.image.load("./content/images/Game/jeff_jumper_down.png").convert_alpha()

    jeffStand = pygame.transform.scale(jeffStand, (jeffStand.get_width() * 1/5, jeffStand.get_height() * 1/5 ))
    jeffJumping = pygame.transform.scale(jeffJumping, (jeffJumping.get_width() * 1/5, jeffJumping.get_height() * 1/5 ))

    self.jeffImage = [jeffStand, jeffJumping]
    self.image = self.jeffImage[0]
    self.w, self.h = windowSize[0], windowSize[1]

    self.rect = self.image.get_rect(midbottom=(self.w // 2, (3*self.h)//4))
    #self.rect = self.image.get_rect(midbottom=(240, 680))

    self.direction = Direction.STATIC

    self.jump_sound = pygame.mixer.Sound("./content/sounds/effects/boing1.mp3")
    self.jump_sound.set_volume(0.1)

  def _input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
     self.direction = Direction.LEFT
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.direction = Direction.RIGHT
    else:
      self.direction = Direction.STATIC

  def _move(self):
    match self.direction:
      case Direction.LEFT:
        self.rect.x -= SPEED
      case Direction.RIGHT:
        self.rect.x += SPEED
      case Direction.STATIC:
        pass
    
    self.rect.x = max(0, min(self.w - self.rect.width, self.rect.x))

  def _gravity(self):
    if not self.jumping:  
        self.velocity += self.gravity
        self.rect.y += self.velocity
        self.velocity = min(self.velocity, 10)
    else:
        self.jump_sound.play()
        self.rect.y -= self.jump_height
        self.jumping = False


  def update(self, collisions):
    self._input()
    self._move()
    self._gravity()

    if collisions:
      self.jumping = True
      self.velocity = -self.jump_height

    if self.rect.y < self.h / 2:
      self.score += 1

  def get_score(self):
    return self.score
  
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    STATIC = 3

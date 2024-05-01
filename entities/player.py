import pygame
from config import quitGame

SPEED = 7
JUMP_HEIGHT = 15
GRAVITY = 0.4

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

  def __init__(self, windowSize, x, y):
    super().__init__()

    self.die = False
    self.jumping = False
    self.jump_height = JUMP_HEIGHT
    self.velocity = self.jump_height
    self.gravity = GRAVITY
    self.friction = -0.10

    self.windowSize = windowSize


    jeffStand =  pygame.image.load("./content/images/Game/jeff_jumper_up.png").convert_alpha()
    jeffJumping =  pygame.image.load("./content/images/Game/jeff_jumper_down.png").convert_alpha()

    jeffStand = pygame.transform.scale(jeffStand, (jeffStand.get_width() * 1/5, jeffStand.get_height() * 1/5 ))
    jeffJumping = pygame.transform.scale(jeffJumping, (jeffJumping.get_width() * 1/5, jeffJumping.get_height() * 1/5 ))

    self.jeffImage = [jeffStand, jeffJumping]
    self.image = self.jeffImage[0]
    self.w, self.h = windowSize[0], windowSize[1]

    self.rect = self.image.get_rect(midbottom=(x, y-100))
    
    self.pos = vec(x,y-100)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    
    self.jump_sound = pygame.mixer.Sound("./content/sounds/effects/boing1.mp3")
    self.jump_sound.set_volume(0.1)

  def _input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
      self.pos.x -= SPEED
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.pos.x += SPEED
    elif keys[pygame.K_ESCAPE]:
      self.pause = True
    else:
      self.pause = False

  def _jump(self):
    self.vel.y = -self.jump_height

  def _gravity(self):
    self.acc = vec(0, self.gravity)

    self.acc.x += self.vel.x * self.friction

    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc

    if self.pos.x > self.windowSize[0]:
        self.pos.x = 0
    if self.pos.x < 0:
        self.pos.x = self.windowSize[0]

    self.rect.midbottom = self.pos

  def update(self, collisions):

    self._input()
    self._gravity()

    if collisions:
      self.jump_sound.play()
      self._jump()

    if self.rect.top > self.windowSize[1]:
      quitGame()
          
  def get_score(self):
    return self.score
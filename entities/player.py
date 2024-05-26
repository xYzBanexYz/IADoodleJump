import pygame
from config import SPEED, JUMP_HEIGHT, GRAVITY, FRICTION, WINDOW_SIZE, quitGame


vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

  def __init__(self, x, y):
    super().__init__()
    self.die = False
    self.jumping = False
    self.jump_height = JUMP_HEIGHT
    self.collisions = False

    jeffStand =  pygame.image.load("./content/images/Game/jeff_jumper_up.png").convert_alpha()
    jeffJumping =  pygame.image.load("./content/images/Game/jeff_jumper_down.png").convert_alpha()
    jeffSauce = pygame.image.load("./content/images/Game/jeffSauce.png").convert_alpha()

    self.jeffImage = [jeffStand, jeffJumping, jeffSauce]
    self.image = self.jeffImage[0]
    self.rect = self.image.get_rect(midbottom=(x, y-100))
    
    self.pos = vec(x,y-100)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    
    self.boingSound = pygame.mixer.Sound("./content/sounds/effects/boing.mp3")
    self.boingSound.set_volume(0.3)

    self.springSound = pygame.mixer.Sound("./content/sounds/effects/spring.mp3")
    self.springSound.set_volume(0.1)

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

  def jump(self, boost=1):
    if boost != 1:
      self.springSound.play()
    else:
      self.boingSound.play()
    self.vel.y = -self.jump_height*boost


  def _gravity(self):
    self.acc = vec(0, GRAVITY)

    self.acc.x += self.vel.x * FRICTION

    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc

    if self.pos.x > WINDOW_SIZE[0]:
        self.pos.x = 0
    if self.pos.x < 0:
        self.pos.x = WINDOW_SIZE[0]

    self.rect.midbottom = self.pos

  def update(self):

    self._input()
    self._gravity()

    if self.vel.magnitude() >= 7:
      self.image = self.jeffImage[1]
    else:
      self.image = self.jeffImage[0]


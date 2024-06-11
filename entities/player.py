import pygame
from config import SPEED, JUMP_HEIGHT, GRAVITY, FRICTION, WINDOW_SIZE, quitGame

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
  """Represents the player character in the game."""

  def __init__(self, x, y):
    """
    Initializes a new instance of the Player class.

    Args:
      x (int): The initial x-coordinate of the player.
      y (int): The initial y-coordinate of the player.
    """
    super().__init__()
    self.die = False
    self.jumping = False
    self.jump_height = JUMP_HEIGHT
    self.collisions = False

    jeffStand = pygame.image.load("./content/images/Game/jeff_jumper_up.png").convert_alpha()
    jeffJumping = pygame.image.load("./content/images/Game/jeff_jumper_down.png").convert_alpha()
    jeffSauce1 = pygame.image.load("./content/images/Game/jeffSauce1.png").convert_alpha()
    jeffSauce2 = pygame.image.load("./content/images/Game/jeffSauce2.png").convert_alpha()

    self.jeffImage = [jeffStand, jeffJumping]
    self.jeffSauceImages = [jeffSauce1, jeffSauce2]
    self.image = self.jeffImage[0]
    self.rect = self.image.get_rect(midbottom=(x, y-100))
    
    self.pos = vec(x, y-100)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    
    self.sauce = False
    self.sauceTime = 0
    self.sauceDuration = 2000
    self.sauceSound = pygame.mixer.Sound("./content/sounds/effects/sauce.mp3")
    self.sauceSound.set_volume(0.3)
    self.sauceIndex = 0
    self.sauceAnimTime = 100  
    self.sauceLastFrameTime = 0

    self.boingSound = pygame.mixer.Sound("./content/sounds/effects/boing.mp3")
    self.boingSound.set_volume(0.3)

    self.springSound = pygame.mixer.Sound("./content/sounds/effects/spring.mp3")
    self.springSound.set_volume(0.1)

  def _input(self):
    """
    Handles the player's input.

    This method checks for keyboard input and updates the player's position accordingly.
    """
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
    """
    Makes the player jump.

    Args:
      boost (float, optional): The boost factor applied to the jump. Defaults to 1.
    """
    if boost != 1:
      self.springSound.play()
    else:
      self.boingSound.play()
    self.vel.y = -self.jump_height * boost

  def _gravity(self):
    """
    Applies gravity to the player.

    This method updates the player's position based on gravity and velocity.
    """
    if not self.sauce:
      self.acc = vec(0, GRAVITY)
    else:
      self.acc = vec(0, -GRAVITY*0.8 / 2) 

    self.acc.x += self.vel.x * FRICTION
    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc

    if self.pos.x > WINDOW_SIZE[0]:
      self.pos.x = 0
    if self.pos.x < 0:
      self.pos.x = WINDOW_SIZE[0]

    self.rect.midbottom = self.pos

  def update(self):
    """
    Updates the player's state.

    This method is called every frame to update the player's position and animation.
    """
    self._input()
    self._gravity()

    if self.sauce:
      self._animate_sauce()
    elif self.vel.magnitude() >= 7:
      self.image = self.jeffImage[1]
    else:
      self.image = self.jeffImage[0]

    if self.sauce:
      current_time = pygame.time.get_ticks()
      if current_time - self.sauceTime > self.sauceDuration:
        self.sauce = False  

  def sauceJump(self):
    """
    Activates the sauce power-up.

    This method enables the sauce power-up and plays the sauce sound effect.
    """
    self.sauce = True
    self.sauceTime = pygame.time.get_ticks() 
    self.sauceSound.play()
  
  def _animate_sauce(self):
    """
    Animates the sauce power-up.

    This method updates the player's image to animate the sauce power-up.
    """
    current_time = pygame.time.get_ticks()
    
    if current_time - self.sauceLastFrameTime > self.sauceAnimTime:
      self.sauceIndex = (self.sauceIndex + 1) % len(self.jeffSauceImages)
      self.image = self.jeffSauceImages[self.sauceIndex]
      self.sauceLastFrameTime = current_time
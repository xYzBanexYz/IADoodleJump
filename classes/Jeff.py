import pygame
from pygame.math import Vector2
import random

from config import WINDOW_SIZE, PADDING, SCROLL_HEIGHT, clock, display, quitGame
from entities.player import Player
from entities.ennemy import Ennemy
from entities.spring import Spring 
from entities.sauce import Sauce 
from classes.platforms import Platforms, Nevada, MovingFrite
from classes.button import Button

pygame.font.init()
font = pygame.font.Font("./content/fonts/PixelifySansSemiBold.ttf", 20)
fontGameOver = pygame.font.Font("./content/fonts/PixelifySansSemiBold.ttf", 50)

class JeffGame:
  """
  The main class representing the Jeff Jump game.
  """

  def __init__(self):
    """
    Initializes the game by setting up the initial game state.
    """
    self.restartGame(menu=True)

  def restartGame(self, menu=False):
    """
    Restarts the game by resetting the game state.

    Parameters:
    - menu (bool): Whether to show the menu screen after restarting the game.
    """
    self.pause = False
    self.menu = menu
    self.restart = False
    self.ennemy = False
    self.gameOver = False
    firstPos = (random.randrange(50, WINDOW_SIZE[0] - 50), random.randrange(SCROLL_HEIGHT + 30, WINDOW_SIZE[1] - 50))

    self.player = pygame.sprite.GroupSingle(Player(*firstPos))
    
    self.allSprites = pygame.sprite.Group()
    self.allSprites.add(self.player, Platforms(*firstPos), Platforms(firstPos[0] - 100, firstPos[1] - 270))
    
    for _ in range(4):
      platform = self.genPlatforms(False, firstPos)
      if platform:
        self.allSprites.add(platform)

    for _ in range(50):
      platform = self.genPlatforms()
      if platform:
        self.allSprites.add(platform)

    self.background = pygame.image.load("./content/images/Game/back.png").convert()
    self.score = 1
    self.count = 0

  def play_step(self):
    """
    Executes a single step of the game loop.

    This function handles user input, updates the game state, and renders the game.
    """
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quitGame()
      elif event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_ESCAPE:
          self.pause =  True

    if not self.gameOver:
      self._update()
      self.player.update()
      self._checkCollisions()
      self._climb()
    else:
      self.gameOverScreen()

    clock.tick(60)

  def _update(self):
    """
    Updates the game display by rendering the background, score, and all sprites.
    """
    display.blit(self.background, (0,0))

    text = font.render(f"Score: {self.score}", False, "BLACK")
    display.blit(text, [5, 5])
    self.allSprites.draw(display)
    pygame.display.update()
  
  def _checkCollisions(self):
    """
    Checks for collisions between the player and other sprites in the game.

    This function handles collision logic for springs, sauces, platforms, enemies, and other special sprites.
    """
    player_sprite = self.player.sprite
    for spr in self.allSprites:
      if isinstance(spr, Spring):
        if pygame.sprite.collide_rect(player_sprite, spr) and spr.low == False:
          if self.player.sprite.rect.bottom <= spr.rect.center[1]: 
            self.player.sprite.jump(2)
            spr.lower()

      if isinstance(spr, Sauce):
        if pygame.sprite.collide_rect(player_sprite, spr):
          if self.player.sprite.rect.bottom <= spr.rect.center[1]: 
            self.player.sprite.sauceJump()
            self.allSprites.remove(spr)

      if isinstance(spr, Platforms):
        if pygame.sprite.collide_rect(player_sprite, spr):
          if self.player.sprite.rect.bottom <= spr.rect.center[1]: 
            self.player.sprite.jump()
            if isinstance(spr, Nevada):
              spr.crash()

        if spr.rect.y >= WINDOW_SIZE[1]:
          self.allSprites.remove(spr)

      if (isinstance(spr, Nevada) and spr.crashed) or isinstance(spr, MovingFrite):
        spr.move()

      if isinstance(spr, Ennemy):
        spr.move()
        if pygame.sprite.collide_rect(player_sprite, spr):
          self.gameOver = True
          self.player.sprite.die = True

          self.playLoseMusic()
        if spr.rect.y > WINDOW_SIZE[1]:
          self.allSprites.remove(spr)
          self.ennemy = False

  def _climb(self):
    """
    Handles the climbing behavior of the player.

    This function moves the player and all sprites upwards when the player reaches the top of the screen.
    It also generates new platforms and enemies as the player climbs higher.
    """
    if self.player.sprite.rect.top < SCROLL_HEIGHT:
      self.player.sprite.pos.y += abs(self.player.sprite.vel.y)
      
      for spr in self.allSprites:
        spr.rect.y += abs(self.player.sprite.vel.y)

        if isinstance(spr, Platforms):
          
          if spr.rect.top > WINDOW_SIZE[1]:
            if (spr.spring != None):
              spr.spring.kill()
              del spr.spring
            elif (spr.sauce != None):
              spr.sauce.kill()
              del spr.sauce
            spr.kill()
            del spr

            self.score += 10

            new_plat = self.genPlatforms()
            if new_plat:
              self.allSprites.add(new_plat)
              if new_plat.spring != None:
                self.allSprites.add(new_plat.spring)
              elif new_plat.sauce != None:
                self.allSprites.add(new_plat.sauce)
    
      if not self.ennemy:
        rnd = random.randint(0,100)
        if rnd > 95 and self.score % 2 == 1:
          x, y = random.randint(0, WINDOW_SIZE[0]), random.randint(-100, -20)
          self.allSprites.add(Ennemy(x, y))
          self.ennemy = True

    elif self.player.sprite.rect.bottom > WINDOW_SIZE[1]:
      self.count += abs(self.player.sprite.vel.y)
      self.player.sprite.pos.y -= abs(self.player.sprite.vel.y)
      
      for spr in self.allSprites:
        spr.rect.y -= abs(self.player.sprite.vel.y)

      if self.count > 1500:
        self.gameOver = True
        self.player.sprite.die = True

        self.playLoseMusic()
        for spr in self.allSprites:
          self.allSprites.remove(spr)
          spr.kill()
      
    if len(self.allSprites) < 50:
      plat = self.genPlatforms()
      if plat:
        self.allSprites.add(plat)

  def genPlatforms(self, top=True, firstPos=None):
    """
    Generates a new platform.

    Parameters:
    - top (bool): Whether the platform should be generated at the top of the screen.
    - firstPos (tuple): The position of the first platform.

    Returns:
    - The generated platform sprite, or None if no platform was generated.
    """
    x = random.randint(100, WINDOW_SIZE[0] - 100)

    plats = [plat for plat in self.allSprites if isinstance(plat, Platforms)]

    if plats:
      plats.sort(key=lambda plat: plat.rect.y, reverse=True)
      miniPlat_x, miniPlat_y = plats[-1].rect.x, plats[-1].rect.y

      upHeight = -5000
      if miniPlat_y < upHeight:
        miniPlat_y = upHeight

      mini = Vector2(miniPlat_x, miniPlat_y)

      attemps = 0
      good = False

      while not good and attemps < 100:
        if top:
          y = random.randint(upHeight, miniPlat_y)
        else:
          y = random.randint(0, firstPos[1])

        current = Vector2(x, y)
        dist = current.distance_to(mini)

        if 100 < dist < 250:
          good = True

        attemps += 1

      if not good:
        return None

      proba = random.randint(0,100)
      if proba > 75:
        return MovingFrite(x,y)
      elif 50 < proba <= 75:
        return Nevada(x,y)
      else:
        return Platforms(x,y)
      
    elif len(self.allSprites) < 6 and top:
      y = random.randint(0,WINDOW_SIZE[1])
      proba = random.randint(0,100)
      if proba > 75:
        return MovingFrite(x,y)
      elif 50 < proba <= 75:
        return Nevada(x,y)
      else:
        return Platforms(x,y)
      
    else:
      return None
    
  def gameOverScreen(self):
    """
    Displays the game over screen.

    This function shows the player's score, a game over message, and buttons to restart the game or go back to the menu.
    """
    pygame.mouse.set_visible(1)
    text = fontGameOver.render(f"Score: {self.score}", True, "BLACK")
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 130))

    textPng = pygame.image.load("./content/images/Menu/OverText.png").convert_alpha()
    textPngRect = textPng.get_rect(topleft=(30,30))

    self.jeffNiceTry = pygame.image.load("./content/images/Menu/niceTry.png").convert_alpha()
    self.jeffNiceTryRect = self.jeffNiceTry.get_rect(bottomleft=(0, WINDOW_SIZE[1]))

    restart_image = pygame.image.load("./content/images/Menu/GameOverRestart.png").convert_alpha()
    self.restart_btn = Button(WINDOW_SIZE[0] // 2 + 50 , WINDOW_SIZE[1] //2 , restart_image,0.9)

    menu_image = pygame.image.load("./content/images/Menu/GameOverMenu.png").convert_alpha()
    self.menu_btn = Button(WINDOW_SIZE[0] // 2 + 150 , WINDOW_SIZE[1] //2 + 130 , menu_image,0.9)

    display.blit(self.background, (0,0))
    display.blit(self.jeffNiceTry, self.jeffNiceTryRect)
    display.blit(text, text_rect)
    display.blit(textPng, textPngRect)

    self.restart_btn.draw(display)
    self.menu_btn.draw(display)

    if self.restart_btn.click():
      self.lose.stop()
      self.restartGame()

    if self.menu_btn.click():
      self.lose.stop()

      self.menu = True
      self.restartGame(True)

    pygame.display.update()

  def playLoseMusic(self):
    """
    Plays the lose music when the player loses the game.
    """
    pygame.mixer.stop()
    self.lose = pygame.mixer.Sound("./content/sounds/effects/lose.mp3")
    self.lose.set_volume(0.1)
    self.lose.play()


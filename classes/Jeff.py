import pygame
import random

from config import WINDOW_SIZE, PADDING, clock, display, quitGame
from entities.player import Player
from entities.ennemy import Ennemy
from entities.spring import Spring 
from classes.platforms import Platforms, Nevada, MovingFrite
from classes.button import Button

pygame.font.init()
font = pygame.font.Font("./content/fonts/PixelifySansSemiBold.ttf", 20)
fontGameOver = pygame.font.Font("./content/fonts/PixelifySansSemiBold.ttf", 50)


class JeffGame:
  def __init__(self):
    self.restartGame(menu=True)

  def restartGame(self, menu=False):
    self.pause = False
    self.menu = menu
    self.restart = False
    self.ennemy = False
    self.gameOver = False

    firstPos = (random.randrange(50, WINDOW_SIZE[0] - 50), random.randrange(WINDOW_SIZE[1] // 2, WINDOW_SIZE[1] - 50))

    self.player = pygame.sprite.GroupSingle(Player(*firstPos))
    
    self.allSprites = pygame.sprite.Group()
    self.allSprites.add(self.player, Platforms(*firstPos), Platforms(firstPos[0] - 100, firstPos[1] - 270))
    
    for i in range(4):
        platform = self.genPlatforms(False)
        if platform:
            self.allSprites.add(platform)

    for i in range(4):
        platform = self.genPlatforms()
        if platform:
            self.allSprites.add(platform)

    self.background = pygame.image.load("./content/images/Game/back.png").convert()
    self.score = 1
    self.count = 0


  def play_step(self):
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
    display.blit(self.background, (0,0))

    text = font.render(f"Score: {self.score}", False, "BLACK")
    display.blit(text, [5, 5])

    self.allSprites.draw(display)
    pygame.display.update()
  
  def _checkCollisions(self):
    player_sprite = self.player.sprite
    for spr in self.allSprites:
      if isinstance(spr, Spring):
        if pygame.sprite.collide_rect(player_sprite, spr) and spr.low == False:
          if self.player.sprite.rect.bottom <= spr.rect.center[1]: 
            self.player.sprite.jump(2)
            spr.lower()

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
          self.playLoseMusic()
        if spr.rect.y > WINDOW_SIZE[1]:
          self.allSprites.remove(spr)
          self.ennemy = False


  def _climb(self):
    if self.player.sprite.rect.top < WINDOW_SIZE[1] // 4:
      self.player.sprite.pos.y += abs(self.player.sprite.vel.y)
      
      # Search for platforms to move
      for spr in self.allSprites:
          spr.rect.y += abs(self.player.sprite.vel.y)

          if isinstance(spr, Platforms):
            
            if spr.rect.top > WINDOW_SIZE[1]:
                # Supprime si la plateforme n'est plus sur l'écran
                if (spr.spring != None):
                  self.allSprites.remove(spr.spring)
                self.allSprites.remove(spr)
                spr.kill()
                self.score += 10

                # Ajoute une nouvelle plateforme pour compenser
                new_plat = self.genPlatforms()
                if new_plat:
                  self.allSprites.add(new_plat)
                  if new_plat.spring != None:
                    self.allSprites.add(new_plat.spring)
      
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
        self.playLoseMusic()
        for spr in self.allSprites:
          self.allSprites.remove(spr)
          spr.kill()

  def genPlatforms(self, top=True):
    x = random.randint(65, WINDOW_SIZE[0] - 65) # la moitié d'une plateforme fait 55px, ici avec une marge de 10
 
    bad_ys = []
    for plat in self.allSprites:
      if isinstance(plat, Platforms):
        bad_ys.append((plat.rect.y-PADDING, plat.rect.y + PADDING + plat.rect.height))

    bad_ys.append((self.player.sprite.pos[1] - PADDING, self.player.sprite.pos[1] + PADDING + self.player.sprite.rect.height))    
    max_attempts = 1000
    attemps = 0
    good = False

    while not good and attemps < max_attempts:
      if top:
        y = random.randint(-200, 50)
      else:
        y = random.randint(0,WINDOW_SIZE[1] // 2)

      good = True
      for bad_y in bad_ys:
        if bad_y[0] <= y <= bad_y[1]:
          good = False
          break
      
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
    
  def gameOverScreen(self):
    

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
    pygame.mixer.music.pause()
    self.lose = pygame.mixer.Sound("./content/sounds/effects/lose.mp3")
    self.lose.set_volume(0.1)
    self.lose.play() 
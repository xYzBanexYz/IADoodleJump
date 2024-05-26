import pygame
from random import randint
class Ennemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./content/images/Game/tucheDaddy.png").convert_alpha()
        self.rect = self.image.get_rect(center= (x,y))
    
    def move(self):
        self.rect.x += (randint(-3, 3))
        self.rect.y += (randint(-3, 3))

    

    
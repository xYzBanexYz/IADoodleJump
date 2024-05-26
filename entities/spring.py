import pygame

class Spring(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./content/images/Game/springHigh.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x,y+10))
        self.low = False

    def lower(self):
        self.image = pygame.image.load("./content/images/Game/springLow.png").convert_alpha()
        self.low = True

import pygame

class Sauce(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.image.load("./content/images/Game/sauce.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x,y+10))

    # TODO!
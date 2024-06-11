import pygame

class Sauce(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initializes a Sauce object.

        Args:
            x (int): The x-coordinate of the Sauce object.
            y (int): The y-coordinate of the Sauce object.
        """
        super().__init__()
        self.image = pygame.image.load("./content/images/Game/sauce.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y+10))

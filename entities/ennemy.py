import pygame
from random import randint
class Ennemy(pygame.sprite.Sprite):
    """Represents an enemy sprite in the game."""

    def __init__(self, x, y):
        """
        Initializes a new instance of the Ennemy class.

        Args:
            x (int): The x-coordinate of the enemy's initial position.
            y (int): The y-coordinate of the enemy's initial position.
        """
        super().__init__()
        image = pygame.image.load("./content/images/Game/tucheDaddy.png").convert_alpha()
        self.image = pygame.transform.scale_by(image, 0.8)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = self.rect.width//2 - 5
    
    def move(self):
        """
        Moves the enemy sprite randomly.

        The enemy sprite is moved by a random amount in both the x and y directions.
        """
        self.rect.x += (randint(-3, 3))
        self.rect.y += (randint(-3, 3))
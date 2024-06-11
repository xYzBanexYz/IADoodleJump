import pygame

class Spring(pygame.sprite.Sprite):
    """
    Represents a spring entity in the game.
    """

    def __init__(self, x, y):
        """
        Initializes a new instance of the Spring class.

        Args:
            x (int): The x-coordinate of the spring's position.
            y (int): The y-coordinate of the spring's position.
        """
        super().__init__()
        self.image = pygame.image.load("./content/images/Game/springHigh.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y + 10))
        self.low = False

    def lower(self):
        """
        Lowers the spring by changing its image to a low spring image.
        """
        self.image = pygame.image.load("./content/images/Game/springLow.png").convert_alpha()
        self.low = True


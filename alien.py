import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Create Alien"""

    def __init__(self, ai_settings, screen) -> None:
        """Initialize Alien and its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the Alien image and set its rect attribute
        self.image = pygame.image.load("./resources/alien.png")
        self.DEFAULT_IMAGE_SIZE = (50, 50)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Start each new alien near top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the Alien exact position
        self.x = float(self.rect.x)


    def blit_me(self):
        """Draw the alien at its position"""
        self.screen.blit(self.image, self.rect)
import pygame


class Ship:
    
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect
        self.image = pygame.image.load("./resources/ship.png")
        self.DEFAULT_IMAGE_SIZE = (100, 100)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect() 

        # Start each new ship at the bottom center of the screen
        self.rect.center = self.screen_rect.center
        self.rect.bottom = self.screen_rect.bottom

        # Store decimal value for the ship's center
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        
        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update movement of the ship."""
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.y -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ai_settings.ship_speed_factor

        # Update the rect object from center
        if self.moving_up or self.moving_down:
            self.rect.y = self.y
        if self.moving_left or self.moving_right:
            self.rect.x = self.x

    def blit_me(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
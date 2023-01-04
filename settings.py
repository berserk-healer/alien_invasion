class Settings:
    """A class to store all settings for Alien Invasions."""

    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Speed settings
        self.ship_speed_factor = 1.5

        # Bullets settings
        self.bullet_speed_factor = 1
        self.bullet_width = 10
        self.bullet_height = 20
        self.bullet_color = (255, 255, 255)



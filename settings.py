class Settings:
    """A class to store all settings for Alien Invasions."""

    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullets settings
        self.bullet_speed_factor = 3
        self.bullet_width = 10
        self.bullet_height = 20
        self.bullet_color = 255, 0, 0

        # Alien Settings
        self.alien_speed_factor = 0.8

        # Fleet settings
        self.fleet_drop_speed = 50
        self.fleet_direction = 1 # fleet_direction = 1 represent right, fleet_direction = 1 represent left


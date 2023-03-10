class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start game at inactive state
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during our game."""
        self.ships_left = self.ai_settings.ship_limit

    

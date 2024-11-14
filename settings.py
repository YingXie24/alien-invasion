# Module that initialises attributes controlling the game's appearance and the ship's speed. 
# Storing settings in a separate class allows us to adjust them more easily.

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialise the game's settings using attributes."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (144, 174, 173)

        # Ship settings
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
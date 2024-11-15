# Module that initialises attributes controlling the game's appearance and the ship's speed. 
# Storing settings in a separate class allows us to adjust them more easily.
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialise the game's settings using attributes."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 22, 34)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_color = (255,131,37)
        self.bullets_allowed = 100

        # Alien settings
        self.alien_speed = 0.1
        self.fleet_drop_speed = 20
        #  fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Pause settings when alien hits ship
        self.pause_time = 1
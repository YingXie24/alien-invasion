# Module that initialises attributes controlling the game's appearance and the ship's speed. 
# Storing settings in a separate class allows us to adjust them more easily.
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialise the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 22, 34)

        # Ship settings
        self.ship_limit = 2

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_color = (255,131,37)
        self.bullets_allowed = 100

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the aliens speed up (multiplier)
        self.speedup_scale = 1.4

        # How quickly the value of aliens increases (multiplier).
        self.score_scale = 2.0

        # Pause settings when alien hits ship
        self.pause_time = 1

        # Call the starting speed method to set up the values as attributes. 
        self.starting_speed()

    def starting_speed(self):
        """Set up the initial settings. 
        These settings will change throughout the game.
        """
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.alien_speed = 0.5

        # Scoring
        self.alien_points = 50

        #  fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed and alien points."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

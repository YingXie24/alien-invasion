import pygame

class Ship:
    """A class to manage the ship."""

    # Take an input, ai_game, for reference to the current instance of the AlienInvasion class.
    def __init__(self, ai_game):
        """Initialise the ship and set its starting position."""

        # Assign the game screen to an attribute of Ship so to access it easily later.
        self.screen = ai_game.screen

        # Access the game screen's rect attribute.
        self.screen_rect = ai_game.screen.get_rect()

        # Load an image of a rocket ship. 
        # Then get the rectangle (rect) of the image.
        self.image = pygame.image.load("images/ship_compressed.bmp")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flag 
        self.moving_right = False
    
    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right:
            self.rect.x += 1

    def blitme(self):
        """Draw the ship to the screen at the position specified by self.rect"""
        self.screen.blit(self.image, self.rect)
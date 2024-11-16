import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    # Take an input, ai_game, for reference to the current instance of the AlienInvasion class.
    def __init__(self, ai_game):
        """Initialise the ship and set its starting position."""
        super().__init__()

        # Assign the game screen to an attribute of Ship to access it easily later.
        self.screen = ai_game.screen

        # Assign settings to an sttribute of Ship. 
        self.settings = ai_game.settings

        # Access the game screen's rect attribute.
        self.screen_rect = ai_game.screen.get_rect()

        # Load an image of a rocket ship. 
        # Then get the rectangle (rect) of the image.
        self.image = pygame.image.load("images/ship_compressed.bmp")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Convert the ship's horizontal position (self.rect.x) into decimal values.
        self.x = float(self.rect.x)

        # Movement flag 
        # The default is False, which means the ship is not moving.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship to the screen at the position specified by self.rect"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        # Initialise the background settings for Pygame to work properly.
        pygame.init()

        # Create an instance of Settings so that we can use it to access settings later
        self.settings = Settings()

        # Create a display window.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance of Ship. 
        # Note Ship() requires one argument, an instance of AlienInvasion
        self.ship = Ship(self)

        # Save background colour as an attribute
        self.bg_color = self.settings.bg_color

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Detect when the arrow key is pressed
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                # Detect when the arrow key is released
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self): 
        """Update images on the screen, and flip to the new screen."""
        # Fill the screen with background color during each pass through the loop.
        self.screen.fill(self.bg_color)

        # Draw the ship on the screen, so the ship appears on top of the background.
        self.ship.blitme()   

        # Make the most recently drawn screen visible.
        # Continually update the display to show the new positions of game elements. 
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
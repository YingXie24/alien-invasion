# The only file to run to play Alien Invasion.

import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        # Initialise the background settings for Pygame to work properly.
        pygame.init()

        # Create an instance of Settings so that we can use it to access settings later
        self.settings = Settings()

        #  Assign the main display surface to 'screen'.
        # Allow running the game in fullscreen mode
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # Create an instance of Ship. 
        # Note Ship() requires one argument, an instance of AlienInvasion
        self.ship = Ship(self)

        # Create an attribute bulletS to represent a whole group of bullets.
        self.bullets = pygame.sprite.Group()

        # Create an attribute alienS to represent a whole group of aliens.
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Save background colour as an attribute
        self.bg_color = self.settings.bg_color

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses, key releases and mouse events."""
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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have gone pass the top of the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Find the number of aliens in a row.
        # Make one alien to help us make the calculation. It won't be part of the fleet.
        # Spacing between each alien is equal to one alien width.
        # Keep width of one alien to the left of the first alien. 
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        # Create the first row of aliens.
        for alien_number in range(number_aliens_x):
            self._create_alien(alien_number)

    def _create_alien(self, alien_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        self.aliens.add(alien)


    def _update_screen(self): 
        """Update images on the screen, and flip to the new screen."""
        # Fill the screen with background color during each pass through the loop.
        self.screen.fill(self.bg_color)

        # Draw the ship on the screen, so the ship appears on top of the background.
        self.ship.blitme()   

        # Draw all fired bullets to the screen.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        # Continually update the display to show the new positions of game elements. 
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
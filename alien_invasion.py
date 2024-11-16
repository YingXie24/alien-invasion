# The only file to run to play Alien Invasion.

import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Create an instance for the Scoreboard.
        self.sb = Scoreboard(self)

        # Create an instance of Ship. 
        # Note Ship() requires one argument, an instance of AlienInvasion
        self.ship = Ship(self)

        # Create an attribute bulletS to represent a whole group of bullets.
        self.bullets = pygame.sprite.Group()

        # Create an attribute alienS to represent a whole group of aliens.
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Save background colour as an attribute
        self.bg_color = self.settings.bg_color

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
        
            # If all ships have been used up, the game should freeze.
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses, key releases and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Detect when the arrow key is pressed.
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                # Detect when the arrow key is released.
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

                # Detect when the mouse is clicked.
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks on the Play button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # Deactivate the play button when the game is going. 
        if button_clicked and not self.stats.game_active:
            self._start_game()
    
    def _start_game(self):
        """Start a new game."""
        # Reset the game speed.
        self.settings.starting_speed()

        # Reset the game statistics. 
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Hide the mouse cursor when the game is going.
        pygame.mouse.set_visible(False)

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

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
        
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """Respond when a bullet hits an alien."""
        # Check for any bullets that have hit aliens.
        #  If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        # When there is a collision, a dictionary is created.
        if collisions:
            # Key: A single bullet. Value: List of aliens hit by the bullet.
            for aliens_list in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens_list)
            self.sb.prep_score()
            self.sb.check_high_score()
    
        # Check whether the entire alien fleet is destroyed.
        #  If yes, a new fleet should appear.
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at the edge of the screen,
            then update the positions of aliens in the fleet.
             Also check if any alien has hit the ship,
              or hit the bottom of the screen.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for when an alien collides with the ship.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Find the number of aliens in a row.
        # Make one alien to help us make the calculation. It won't be part of the fleet.
        # Spacing between each alien is equal to one alien width.
        # Keep width of one alien to the left of the first alien. 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        #  Leave two alien height from the top, three alien heights from the rocket, 
        #   and the ship height from the bottom of the screen.
        #  Keep gap of one alien height between each row.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (5 * alien_height) 
                             - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        #  Outer loop: Count the number of rows of aliens we want.
        for row_number in range(number_rows):
            # Inner loop: Create one row of aliens.
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.y = (2 * alien_height) + (2 * alien_height * row_number)
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrease the number of ships left, and update the scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clear out all remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause to allow user to regroup.
            sleep(self.settings.pause_time)

        # When player runs out of ship, the game ends.
        else:
            self.stats.game_active = False
            # Make the cursor reappear.
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

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

        # Draw the score information
        self.sb.draw_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        # Continually update the display to show the new positions of game elements. 
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
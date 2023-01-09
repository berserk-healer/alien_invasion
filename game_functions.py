import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button):
    """Respond to keypress and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ai_settings, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, aliens, ship, bullets)


def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, aliens, ship, bullets):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        stats.game_active = True

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        pygame.mouse.set_visible(False)
        
            

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats):
    # Move the ship with arrow keys
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        if not stats.game_active:
            stats.game_active = True
    elif event.key == pygame.K_LSHIFT:
        change_ship_speed(ai_settings, True)


def check_keyup_events(event, ai_settings, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_LSHIFT:
        change_ship_speed(ai_settings, False)
    

def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_me()
    aliens.draw(screen)
    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, aliens, bullets, screen, ship):
    """Update position of bullets and get rid of old bullets"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)
    

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Respond to alien bullet collision."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # Destroy existing bulelts  and create new fleet
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire bullet."""
    new_bullets = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullets)


def change_ship_speed(ai_settings, trigger = False):
    """Change ship speed factor when LSHIFT is pressed"""
    if trigger:
        ai_settings.ship_speed_factor = 0.5
    else:
        ai_settings.ship_speed_factor = 1.5



def get_number_alien_x(ai_settings, alien_width):
    """Calculate number of aliens fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Calculate number of rows"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    numbers_rows = int(available_space_y / (2 * alien_height))
    return numbers_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    """Create a fleet of aliens"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = 5  # get_number_alien_x(ai_settings, alien.rect.width) 
    number_rows = 3 # get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        
        
def check_fleet_edge(ai_settings, aliens):
    """Respond appropriately if aliens reached edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
    

def change_fleet_direction(ai_settings, aliens):
    """Drop entire fleet and change direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens, ship, stats, screen, bullets):
    """Update the position of all aliens on the screen."""
    check_fleet_edge(ai_settings, aliens)
    aliens.update()

    # Look for alien - ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien event."""
    if stats.ships_left > 0:
        # Decrease number of ship left
        stats.ships_left -= 1

        # Empty the lists of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens reach the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
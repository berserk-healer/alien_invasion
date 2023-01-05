import sys
import pygame
from random import randint
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, ship, bullets):
    """Respond to keypress and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ai_settings, ship)
            

def check_keydown_events(event, ai_settings, screen, ship, bullets):
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
    

def update_screen(ai_settings, screen, ship, bullets, aliens):
    """Update images on the screen and flip to the new screen."""
    screen.fill(ai_settings.bg_color)
    # Redraw bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_me()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(bullets):
    """Update position of bullets and get rid of old bullets"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


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
    number_aliens_x =  randint(1, 5) # get_number_alien_x(ai_settings, alien.rect.width) 
    number_rows = randint(1, 3) # get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        
        
        
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from pygame.sprite import Group


def run_game():
    # Initialize game
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    bg = pygame.image.load("./resources/background.jpg")
    bg = pygame.transform.scale(bg, (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make play button
    play_button = Button(ai_settings, screen, "Play")

    stats = GameStats(ai_settings)
    
    # Make a ship, a group of bullets and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()


    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # Start the main loop for the game:
    while True:
        screen.blit(bg, (0,0))
        gf.check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, aliens, bullets, screen, ship)
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button)

        
run_game()

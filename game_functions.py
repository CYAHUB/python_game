import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, game_settings, screen, ship, bullets):
    """Kontrollige sündmuste klõpsu all"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        fire_bullet(game_settings, screen, ship, bullets)
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Kontrolli sündmusi võti üles"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(game_settings, screen, stats, play_button, ship, aliens, bullets):
    """Kontrollige klaviatuuri ja hiire sündmusi"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(game_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        game_settings.init_dynamic_settings()
        stats.game_active = True
        pygame.mouse.set_visible(False)
        aliens.empty()
        bullets.empty()
        create_fleet(game_settings, screen, ship, aliens)
        ship.ship_center()


def update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Värskendage pilti ekraanil ja joonistage uus ekraan"""
    # Lisage ekraani taust
    screen.fill(game_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Lisan laev ekraanile
    ship.blitme()
    # Lisan tulnukas ekraanile
    aliens.draw(screen)
    # Näita Scoreboard
    sb.draw_score()
    # Näita mängu nuppu
    if not stats.game_active:
        play_button.draw_button()
    # Näita viimast ekraani
    pygame.display.flip()


def update_bullets(game_settings, screen, stats, sb, ship, aliens, bullets):
    """Uuendage kuulide asukohta ja eemaldage vanad kuulid"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(game_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(game_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += game_settings.alien_points
        sb.prepare_score()
    # Eemaldage kuulid ja looge uus laevastik
    if len(aliens) == 0:
        bullets.empty()
        game_settings.increase_speed()
        create_fleet(game_settings, screen, ship, aliens)


def fire_bullet(game_settings, screen, ship, bullets):
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(game_settings, alien_width):
    """Arvuta tulnukate arv rida"""
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(game_settings, ship_height, alien_height):
    """Määrake ekraanil olevate ridade arv"""
    available_space_y = game_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(game_settings, screen, aliens, alien_number, row_number):
    # Loo tulnukas ja pane see rida
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(game_settings, screen, ship, aliens):
    """Luua tulnukate laevastik"""
    # Looge tulnukat ja arvutage, kui palju tulnukaid võib järjest eksisteerida
    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)
    # Looge esimene rida
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(game_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def update_aliens(game_settings, stats, screen, ship, aliens, bullets):
    """Tulnukate asukoha uuendamine"""
    check_fleet_edges(game_settings, aliens)
    aliens.update()
    # Kontrollige laeva ja tulnukate kokkupõrkeid
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, ship, aliens, bullets)
    # Kontrolli tulnukate ilmumist ekraani allosas
    check_aliens_bottom(game_settings, stats, screen, ship, aliens, bullets)


def check_aliens_bottom(game_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, stats, screen, ship, aliens, bullets)
            break


def ship_hit(game_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        # Laeva elu miinus üks
        stats.ships_left = stats.ships_left - 1
        # Tulnukade ja kuulide rühmad on tühjad
        aliens.empty()
        bullets.empty()
        # Luua uus välismaalaste laevastik
        create_fleet(game_settings, screen, ship, aliens)
        # Laeva keskus
        ship.ship_center()
        # paus
        sleep(2)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

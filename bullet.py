import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Bullet kontrolli klass"""

    def __init__(self, game_setting, screen, ship):
        """Looge laeva asukohas kuulide objekt"""
        super().__init__()
        self.screen = screen
        # Loovad kuulid
        self.rect = pygame.Rect(0, 0, game_setting.bullet_width, game_setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # kuuli positioon
        self.y = float(self.rect.y)
        # kuuli sätted
        self.color = game_setting.bullet_color
        self.speed_factor = game_setting.bullet_speed_factor

    def update(self):
        """Kuuli positsiooni värskendamine"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Joonistage kuul ekraanil"""
        pygame.draw.rect(self.screen, self.color, self.rect)

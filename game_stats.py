class GameStats:
    """Mängu statistika"""
    def __init__(self, game_settings):
        """Statistika alustamine"""
        self.score = None
        self.ships_left = None
        self.game_settings = game_settings
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        """Alustage statistikat, muutke mängu ajal"""
        self.ships_left = self.game_settings.ship_limit
        self.score = 0

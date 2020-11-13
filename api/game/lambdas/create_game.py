"""
Creates a game, saves it to DB and returns it
"""

from ..models.base_handler import LambdaBase
from ..models.game_models import Game


class CreateGameClass(LambdaBase):
    def process_event(self, event):
        game = Game()
        game.save()
        game.refresh()
        return 200, {"game": game.get_info()}


handler = CreateGameClass.get_handler()

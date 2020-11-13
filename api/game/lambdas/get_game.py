"""
Get game info specified by id
"""

from ..models.base_handler import LambdaBase
from ..models.game_models import Game


class GetGameClass(LambdaBase):
    def process_event(self, event):
        path_parameters = event.get("pathParameters", {})
        game_id = path_parameters.get("game_id")

        try:
            game = Game.get(game_id)
        except Game.DoesNotExist:
            return 404, {"error": "Game not found"}

        return 200, {"game": game.get_info()}


handler = GetGameClass.get_handler()

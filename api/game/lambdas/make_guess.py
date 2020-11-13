"""
Records a player guess, evaluates game completion and returns game info
"""
from ..models.base_handler import LambdaBase
from ..models.game_models import Game, Guess


class MakeGuessClass(LambdaBase):
    def process_event(self, event):
        path_parameters = event.get("pathParameters", {})
        game_id = path_parameters.get("game_id")
        combination = path_parameters.get("guess")

        guess = Guess(combination=combination)

        if not guess.is_valid_guess():
            return 400, {"error": "Invalid guess"}

        try:
            game = Game.get(game_id)
        except Game.DoesNotExist:
            return 404, {"error": "Game not found"}

        if not game.is_playable():
            return 400, {"error": "Game is finished"}

        guess.black_pegs, guess.white_pegs = game.get_black_and_white_pegs(guess)
        game.check_win_condition(guess)
        game.save_guess(guess)
        game.refresh()

        return 200, {"game": game.get_info()}


handler = MakeGuessClass.get_handler()

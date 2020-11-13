import os
from contextlib import contextmanager

from botocore.exceptions import ClientError

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

SUITE_OF_GAMES = [
    {"game_id": "A", "code": "RGGB", "guess": "RGGB", "black_pegs": 4, "white_pegs": 0},
    {"game_id": "B", "code": "RRRR", "guess": "BYOB", "black_pegs": 0, "white_pegs": 0},
    {"game_id": "C", "code": "GBBR", "guess": "GBRB", "black_pegs": 2, "white_pegs": 2},
    {"game_id": "D", "code": "BBBR", "guess": "RBGG", "black_pegs": 1, "white_pegs": 1},
    {
        "game_id": "E",
        "code": "RBGG",
        "guess": "BBBR",
        "black_pegs": 1,
        "white_pegs": 1,
    },
    {"game_id": "F", "code": "BBBR", "guess": "BBRB", "black_pegs": 2, "white_pegs": 2},
    {"game_id": "G", "code": "WBWB", "guess": "BWBW", "black_pegs": 0, "white_pegs": 4},
    {"game_id": "H", "code": "OOOW", "guess": "OWWW", "black_pegs": 2, "white_pegs": 0},
    {"game_id": "I", "code": "OOOW", "guess": "OOOO", "black_pegs": 3, "white_pegs": 0},
]


@contextmanager
def dynamodb_setup(dynamodb):
    dynamodb.create_table(
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
        ],
        TableName=DYNAMODB_TABLE_NAME,
        KeySchema=[
            {"AttributeName": "pk", "KeyType": "HASH"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    yield


class TestMakeGuess:
    def test_table_creation(self, dynamodb):

        with dynamodb_setup(dynamodb):

            try:
                table = dynamodb.Table(DYNAMODB_TABLE_NAME)
                assert table.table_name == DYNAMODB_TABLE_NAME
            except ClientError as err:
                assert err.response["Error"]["Code"] == "ResourceNotFoundException"

    def test_guess_on_non_existent_game(self):
        from ..lambdas.make_guess import MakeGuessClass

        status_code, response_body = MakeGuessClass().process_event(
            {"pathParameters": {"game_id": "TEST", "guess": "RRRR"}}
        )
        assert status_code == 404

    def test_malformatted_guess(self):
        from ..lambdas.make_guess import MakeGuessClass

        status_code, response_body = MakeGuessClass().process_event(
            {"pathParameters": {"game_id": "TEST", "guess": "A"}}
        )
        assert status_code == 400

    def test_correct_guess(self):
        from ..lambdas.create_game import CreateGameClass
        from ..lambdas.make_guess import MakeGuessClass

        create_status_code, create_body = CreateGameClass().process_event({})
        game_id = create_body.get("game").get("game_id")

        (
            make_guess_status_code,
            make_guess_response_body,
        ) = MakeGuessClass().process_event(
            {"pathParameters": {"game_id": game_id, "guess": "RRRR"}}
        )
        assert make_guess_status_code == 200

    def test_set_of_plays(self):
        from ..models.game_models import Game
        from ..lambdas.make_guess import MakeGuessClass

        for game in SUITE_OF_GAMES:
            game_id = game.get("game_id")
            code = game.get("code")
            guess = game.get("guess")
            black_pegs = game.get("black_pegs")
            white_pegs = game.get("white_pegs")

            Game(hash_key=game_id, secret=code).save()

            status_code, response_body = MakeGuessClass().process_event(
                {"pathParameters": {"game_id": game_id, "guess": guess}}
            )

            guesses = response_body.get("game").get("guesses")
            last_guess = guesses.pop()
            last_guess_bp = last_guess.get("black_pegs")
            last_guess_wp = last_guess.get("white_pegs")

            assert black_pegs == last_guess_bp and white_pegs == last_guess_wp

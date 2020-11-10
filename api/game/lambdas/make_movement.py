"""
Records a player movement and evaluates game completion
"""
import os
from datetime import datetime
from json import dumps

import boto3
from aws_lambda_powertools import Logger, Tracer

TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
TOTAL_DIGITS = 4

tracer = Tracer()
logger = Logger()
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


@tracer.capture_lambda_handler
@logger.inject_lambda_context
def handler(event, context) -> dict:
    return process_event(event)


def process_event(event: dict) -> dict:
    path_parameters = event.get("pathParameters", {})
    game_id = path_parameters.get("game_id")
    movement = str(path_parameters.get("movement"))

    if len(movement) != TOTAL_DIGITS:
        return __format_bad_request_error(
            f"Movement must contain {str(TOTAL_DIGITS)} digits"
        )

    game = _get_game(game_id)

    if not game:
        return {"statusCode": 404, "body": dumps({"error": "Game not found"})}

    secret = game.get("secret")
    tries_left = int(game.get("tries_left"))
    solved = game.get("is_solved")

    if solved:
        return __format_bad_request_error("Game is finished")

    if not tries_left:
        return __format_bad_request_error("No tries left")

    correct_position_counter = _count_digits_in_correct_position(secret, movement)
    digit_in_secret_counter = _count_digits_present_in_secret(secret, movement)

    if correct_position_counter == TOTAL_DIGITS:
        solved = True

    _save_movement(game_id, solved)

    return __format_success_response(
        {
            "tries_left": tries_left - 1,
            "correct_position_number": correct_position_counter,
            "digit_present_in_secret": digit_in_secret_counter,
            "is_solved": solved,
        }
    )


def _count_digits_in_correct_position(secret: str, movement: str) -> int:
    counter = 0
    for i, letter in enumerate(secret):
        if movement[i] == letter:
            counter += 1
    return counter


def _count_digits_present_in_secret(secret: str, movement: str) -> int:
    counter = 0
    movement_unique_digits = set(movement)  # Remove duplicates
    for i in movement_unique_digits:
        if i in secret:
            counter += 1
    return counter


def _get_game(game_id: str) -> dict:
    game = table.get_item(Key={"pk": f"GAM#{game_id}"}).get("Item", {})
    return game


def _save_movement(game_id: str, solved: bool) -> None:
    table.update_item(
        Key={
            "pk": f"GAM#{game_id}",
        },
        UpdateExpression="SET #tl = #tl - :one, #lm = :now, #slv = :slv",
        ExpressionAttributeNames={
            "#tl": "tries_left",
            "#lm": "last_movement",
            "#slv": "is_solved",
        },
        ExpressionAttributeValues={
            ":one": 1,
            ":now": datetime.utcnow().isoformat(),
            ":slv": solved,
        },
    )


def __format_bad_request_error(message: str) -> dict:
    return {"statusCode": 400, "body": dumps({"error": message})}


def __format_success_response(message: str) -> dict:
    return {"statusCode": 200, "body": dumps({"message": message})}

"""
Get game info specified by id
"""
import os
from decimal import Decimal
from json import JSONEncoder, dumps

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

    game = _get_game(game_id)

    if not game:
        return {"statusCode": 404, "body": dumps({"error": "Game not found"})}

    return {"statusCode": 200, "body": dumps({"game": game}, cls=DecimalEncoder)}


def _get_game(game_id: str) -> dict:
    game = table.get_item(
        Key={"pk": f"GAM#{game_id}"},
        ProjectionExpression="tries_left, last_movement, is_solved, created_at",
    ).get("Item", {})
    return game


class DecimalEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)

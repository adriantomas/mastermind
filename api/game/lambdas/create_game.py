"""
Creates a game, saves it to DB and returns the id
"""
import os
from datetime import datetime
from json import dumps
from random import randrange
from uuid import uuid4

import boto3
from aws_lambda_powertools import Logger, Tracer

TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
MAX_TRIES = 8

tracer = Tracer()
logger = Logger()
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


@tracer.capture_lambda_handler
@logger.inject_lambda_context
def handler(event, context) -> dict:
    return process_event(event)


def process_event(event: dict) -> dict:
    secret = str(randrange(1000, 10000))
    game_id = str(uuid4())
    _save_game(game_id, secret)

    return {"statusCode": 200, "body": dumps({"game_id": game_id})}


def _save_game(game_id: str, secret: str) -> None:
    table.put_item(
        Item={
            "pk": f"GAM#{game_id}",
            "secret": secret,
            "tries_left": MAX_TRIES,
            "created_at": datetime.utcnow().isoformat(),
        }
    )

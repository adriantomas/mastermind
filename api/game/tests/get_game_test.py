import os
from contextlib import contextmanager
from json import loads

from botocore.exceptions import ClientError

DYNAMODB_TABLE_NAME = "DB_TEST"
os.environ["DYNAMODB_TABLE_NAME"] = DYNAMODB_TABLE_NAME
os.environ["POWERTOOLS_TRACE_DISABLED"] = "true"


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


class TestCreateGame:
    def test_table_creation(self, dynamodb):

        with dynamodb_setup(dynamodb):

            try:
                table = dynamodb.Table(DYNAMODB_TABLE_NAME)
                assert table.table_name == DYNAMODB_TABLE_NAME
            except ClientError as err:
                assert err.response["Error"]["Code"] == "ResourceNotFoundException"

    def test_get_non_existent_game(self):
        from ..lambdas.get_game import process_event

        response = process_event({"pathParameters": {"game_id": "TEST"}})
        assert response.get("statusCode") == 404

    def test_get_existent_game(self):
        from ..lambdas.create_game import process_event as create_game
        from ..lambdas.get_game import process_event as get_game

        response = create_game({})
        body = loads(response.get("body"))
        game_id = body.get("game_id")

        response = get_game({"pathParameters": {"game_id": game_id}})
        assert response.get("statusCode") == 200

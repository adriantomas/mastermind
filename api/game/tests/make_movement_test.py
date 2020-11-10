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


class TestMakeMovement:
    def test_table_creation(self, dynamodb):

        with dynamodb_setup(dynamodb):

            try:
                table = dynamodb.Table(DYNAMODB_TABLE_NAME)
                assert table.table_name == DYNAMODB_TABLE_NAME
            except ClientError as err:
                assert err.response["Error"]["Code"] == "ResourceNotFoundException"

    def test_movement_on_non_existent_game(self):
        from ..lambdas.make_movement import process_event

        response = process_event(
            {"pathParameters": {"game_id": "TEST", "movement": "1234"}}
        )
        assert response.get("statusCode") == 404

    def test_malformatted_movement(self):
        from ..lambdas.make_movement import process_event

        response = process_event(
            {"pathParameters": {"game_id": "TEST", "movement": "1"}}
        )
        assert response.get("statusCode") == 400

    def test_correct_movement(self):
        from ..lambdas.create_game import process_event as create_game
        from ..lambdas.make_movement import process_event as make_movement

        response = create_game({})
        body = loads(response.get("body"))
        game_id = body.get("game_id")

        response = make_movement(
            {"pathParameters": {"game_id": game_id, "movement": "1234"}}
        )
        assert response.get("statusCode") == 200

import os
from contextlib import contextmanager

from botocore.exceptions import ClientError

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")


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
        from ..lambdas.get_game import GetGameClass

        status_code, response_body = GetGameClass().process_event(
            {"pathParameters": {"game_id": "TEST"}}
        )
        assert status_code == 404

    def test_get_existent_game(self):
        from ..lambdas.create_game import CreateGameClass
        from ..lambdas.get_game import GetGameClass

        create_status_code, create_body = CreateGameClass().process_event({})
        game_id = create_body.get("game").get("game_id")

        get_status_code, get_body = GetGameClass().process_event(
            {"pathParameters": {"game_id": game_id}}
        )
        assert get_status_code == 200 and create_body == get_body

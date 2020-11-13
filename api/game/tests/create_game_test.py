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

    def test_game_creation(self):
        from ..lambdas.create_game import CreateGameClass

        status_code, response_body = CreateGameClass().process_event({})
        assert status_code == 200

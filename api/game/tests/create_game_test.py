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

    def test_game_creation(self):
        from ..lambdas.create_game import process_event

        response = process_event({})
        body = loads(response.get("body"))
        assert "game_id" in body

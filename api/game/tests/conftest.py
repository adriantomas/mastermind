import os

import boto3
import pytest
from moto import mock_dynamodb2

DYNAMODB_TABLE_NAME = "DB_TEST"
os.environ["DYNAMODB_TABLE_NAME"] = DYNAMODB_TABLE_NAME
os.environ["POWERTOOLS_TRACE_DISABLED"] = "true"


@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="module")
def dynamodb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.resource("dynamodb", region_name="us-east-1")

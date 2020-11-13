"""
Base class for implementing Lambda handlers.
Adds common logging and tracing capabilities.
"""
from abc import ABC, abstractmethod
from json import dumps
from typing import Tuple
from aws_lambda_powertools import Logger, Tracer

tracer = Tracer()
logger = Logger()


class LambdaBase(ABC):
    @classmethod
    def get_handler(cls, *args, **kwargs) -> dict:
        @tracer.capture_lambda_handler
        @logger.inject_lambda_context
        def handler(event, context) -> dict:
            status_code, response_body = cls(*args, **kwargs).process_event(event)

            if not isinstance(status_code, int):
                raise Exception("Invalid status code")

            if not isinstance(response_body, dict):
                raise Exception("Response body must conform a JSON object")

            response = {"statusCode": status_code, "body": dumps(response_body)}

            logger.debug(response)
            return response

        return handler

    @abstractmethod
    def process_event(self, event: dict) -> Tuple[int, dict]:
        """Lambda logic handler

        Args:
            ``event`` (dict): AWS Lambda event object,

        Raises:
            ``NotImplementedError``: in case of implementation absence

        Returns:
            ``status_code``, ``response_body`` (Tuple[int, dict])

            Example:
                200, {"status": "ok"}
                404, {"error": "not_found"}
        """

        raise NotImplementedError

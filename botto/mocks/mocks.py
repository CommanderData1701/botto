# -*- coding: utf-8 -*-
"""Module containing mock classes for testing purposes."""
# type: ignore
# pylint: disable=all


from typing import Optional
from sqlite3 import Connection
from dataclasses import dataclass


class MockRequest:
    """Mock class for the requests module.
    
    The MockRequest class is a mock class for the requests module. It is used
    to do integration tests.

    Attributes:
        request_cache (list[dict]): List of requests made.
        message_sent (list[dict]): List of messages sent.
        message (MockJson): Object containing the message to be returned.
    """
    class MockJson:
        """Class that mocks the json method of a response."""
        def __init__(self, data: Optional[dict] = None) -> None:
            self.data = data
            self.status_code = 200

        def json(self) -> Optional[dict]:
            """Returns the data of the response."""
            return self.data

    def __init__(self, message: dict) -> None:
        self.request_cache: list[dict] = []
        self.message_sent: list[dict] = []
        self.message = self.MockJson(message)

    def set_message(self, message: dict) -> None:
        """Sets the message to be returned."""
        self.message = self.MockJson(message)

    def get(self, url: str, timeout: int = 5) -> MockJson:
        """Mimics a get request."""
        self.request_cache.append({"url": url, "method": "GET"})
        return self.message
    
    def post(self, url: str, json: dict, timeout: int = 5) -> MockJson:
        """Mimics a post request."""
        self.request_cache.append({"url": url, "method": "POST"})
        self.message_sent.append(json)
        return self.message


@dataclass
class MockObject:
    requests: MockRequest
    db_connection: Connection
    config_file: str

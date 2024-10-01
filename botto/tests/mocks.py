# type: ignore


from typing import Optional
from sqlite3 import Connection
from dataclasses import dataclass


class MockRequest:
    class MockJson:
        def __init__(self, data: Optional[dict] = None) -> None:
            self.data = data
            self.status_code = 200

        def json(self) -> Optional[dict]:
            return self.data

    def __init__(self, message: dict) -> None:
        self.request_cache = []
        self.message_sent = []
        self.message = self.MockJson(message)

    def set_message(self, message: dict) -> None:
        self.message = self.MockJson(message)

    def get(self, url: str, timeout: int = 5) -> MockJson:
        self.request_cache.append({"url": url, "method": "GET"})
        return self.message
    
    def post(self, url: str, json: dict, timeout: int = 5) -> MockJson:
        self.request_cache.append({"url": url, "method": "POST"})
        self.message_sent.append(json)
        return self.message


@dataclass
class MockObject:
    requests: MockRequest
    db_connection: Connection
    config_file: str

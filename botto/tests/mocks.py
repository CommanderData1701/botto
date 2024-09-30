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
        self.message = self.MockJson(message)

    def set_message(self, message: dict) -> None:
        self.message = self.MockJson(message)

    def get(self, _url: str, timeout: int = 5) -> MockJson:
        return self.message


@dataclass
class MockObject:
    requests: MockRequest
    db_connection: Connection
    config_file: str

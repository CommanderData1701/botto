import unittest
import sqlite3

from ..botto import Botto
from ..message import Message


class MockRequest:
    class MockJson:
        def __init__(self, data: dict = None) -> None:
            self.data = data
            self.status_code = 200

        def json(self) -> dict:
            return self.data

    def __init__(self, message: dict) -> None:
        self.message = self.MockJson(message)

    def set_message(self, message: dict) -> None:
        self.message = self.MockJson(message)

    def get(self, _url: str) -> MockJson:
        return self.message


class TestGetMessages(unittest.TestCase):

    def test_get_messages_with_only_messages(self):
        message_dict: dict = {
            "ok": True,
            "result": [
                {"update_id":12, "message":{"message_id":60,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285082,"text":"Bruh"}},
                {"update_id":13, "message":{"message_id":61,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285098,"text":"What\u2018s up ye old bot?"}},
                {"update_id":14, "message":{"message_id":62,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285113,"text":"I have to say that you are not very talkative"}},
                {"update_id":15, "message":{"message_id":63,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285131,"text":"Sheesh! XD lol"}}]
        }
        bot = Botto(
            mock_db_connection=sqlite3.connect(':memory:'),
            mock_requests=MockRequest(message_dict),
            mock_token=True
        )

        bot.get_messages()

        expected_messages = [
            Message(chat_id=42, update_id=12, content="Bruh"),
            Message(chat_id=42, update_id=13, content="What‘s up ye old bot?"),
            Message(chat_id=42, update_id=14, content="I have to say that you are not very talkative"),
            Message(chat_id=42, update_id=15, content="Sheesh! XD lol")
        ]

        for expected, actual in zip(expected_messages, bot.messages):
            self.assertEqual(expected.chat_id, actual.chat_id)
            self.assertEqual(expected.update_id, actual.update_id)
            self.assertEqual(expected.content, actual.content)


if __name__ == '__main__':
    unittest.main()

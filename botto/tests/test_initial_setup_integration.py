import unittest
import sqlite3
import os
from random import seed

from .mocks import MockObject, MockRequest
from ..botto import Botto

seed(42)


class test_initial_setup_integration(unittest.TestCase):
    def test_initial_setup_integration_trivial(self):
        message_dict: dict = {
            "ok": True,
            "result": [
                {"update_id":12, "message":{"message_id":60,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285082,"text":"Hello there!"}},
                {"update_id":13, "message":{"message_id":61,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285098,"text":"John"}},
                {"update_id":14, "message":{"message_id":62,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285113,"text":"yes"}},
                {"update_id":15, "message":{"message_id":63,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285131,"text":"Jane, Joshua"}},
                {"update_id":16, "message":{"message_id":63,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285157,"text":"yes"}}
            ]
        }
        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        mocks = MockObject(
            requests=MockRequest(message_dict),
            db_connection=connection,
            config_file="test_config.json"
        )
        botto = Botto(
            mock=mocks
        )
        botto.get_messages()
        botto.handle_message()

        post_requests = [request for request in mocks.requests.request_cache if request["method"] == "POST"]
        get_requests = [request for request in mocks.requests.request_cache if request["method"] == "GET"]
        self.assertTrue(
            all([request["url"] == "https://api.telegram.org/botABCDEFG/getUpdates" for request in get_requests])
        )
        self.assertTrue(
            all([request["url"] == "https://api.telegram.org/botABCDEFG/sendMessage" for request in post_requests])
        )
        expected_messages = [
            "Hello! You are now the root user. What's your name?",
            "Hello, John! Is this correct? (yes/no)",
            "Great! Now tell us who your roommates are. (Seperated by commas)",
            "Are Jane, Joshua your roommates? (yes/no)",
            "All set!",
        ]
        
        for message, expected in zip(mocks.requests.message_sent[:-1], expected_messages):
            self.assertEqual(message["text"], expected)

        token_message = mocks.requests.message_sent[-1]

        cursor.execute(
                "SELECT name, token FROM users"
        )
        name_token = cursor.fetchall()
        john_token = [token for name, token in name_token if name == "John"][0]
        jane_token = [token for name, token in name_token if name == "Jane"][0]
        joshua_token = [token for name, token in name_token if name == "Joshua"][0]

        expected_token_message = "Here you go! All users and their tokens:\n\n"
        expected_token_message += f"John: {john_token}\n"
        expected_token_message += f"Jane: {jane_token}\n"
        expected_token_message += f"Joshua: {joshua_token}\n\n"
        expected_token_message += "They just need to provide them when writing to me and they can get started!"

        self.assertEqual(token_message["text"], expected_token_message)

        os.remove("test_config.json")


if __name__ == "__main__":
    unittest.main()

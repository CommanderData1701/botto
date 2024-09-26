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
                {"update_id":15, "message":{"message_id":63,"from":{"id":42,"is_bot":False,"first_name":"Max Mustermann","language_code":"de"},"chat":{"id":42,"first_name":"Max Mustermann","type":"private"},"date":285131,"text":"Sheesh! XD lol"}}
            ]
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
            

    def test_messages_with_non_text_messages_and_different_users(self) -> None:
        message_dict: dict = {
            "ok": True,
            "result": [
                {"update_id":100, "message":{"message_id":200,"from":{"id":101,"is_bot":False,"first_name":"Alice","language_code":"en"},"chat":{"id":101,"first_name":"Alice","type":"private"},"date":1695700010,"text":"Hey, how are you doing?"}},
                {"update_id":101, "message":{"message_id":201,"from":{"id":102,"is_bot":False,"first_name":"Bob","language_code":"fr"},"chat":{"id":102,"first_name":"Bob","type":"private"},"date":1695700110,"photo":[
                    {"file_id":"PHOTO_123", "file_unique_id":"PHOTO_UNIQUE_123", "file_size":204800, "width":1280, "height":720}
                ], "caption": "Check out this amazing view!"}},
                {"update_id":102, "message":{"message_id":202,"from":{"id":103,"is_bot":False,"first_name":"Charlie","language_code":"es"},"chat":{"id":103,"first_name":"Charlie","type":"private"},"date":1695700210,"sticker":
                    {"file_id":"STICKER_456", "file_unique_id":"STICKER_UNIQUE_456", "width":512, "height":512, "is_animated":True, "thumb":{"file_id":"THUMB_456", "file_unique_id":"THUMB_UNIQUE_456", "file_size":10240, "width":128, "height":128}}
                }},
                {"update_id":103, "message":{"message_id":203,"from":{"id":104,"is_bot":False,"first_name":"Diana","language_code":"ru"},"chat":{"id":104,"first_name":"Diana","type":"private"},"date":1695700310,"voice":
                    {"file_id":"VOICE_789", "file_unique_id":"VOICE_UNIQUE_789", "duration":25, "mime_type":"audio/mpeg", "file_size":50960}
                }},
                {"update_id":104, "message":{"message_id":204,"from":{"id":105,"is_bot":False,"first_name":"Eve","language_code":"it"},"chat":{"id":105,"first_name":"Eve","type":"private"},"date":1695700410,"document":
                    {"file_id":"DOC_001", "file_unique_id":"DOC_UNIQUE_001", "file_name":"project.pdf", "mime_type":"application/pdf", "file_size":204800}
                }},
                {"update_id":105, "message":{"message_id":205,"from":{"id":106,"is_bot":False,"first_name":"Frank","language_code":"en"},"chat":{"id":106,"first_name":"Frank","type":"private"},"date":1695700510,"text":"Just got this new song. What do you think?"}},
                {"update_id":106, "message":{"message_id":206,"from":{"id":107,"is_bot":False,"first_name":"Grace","language_code":"de"},"chat":{"id":107,"first_name":"Grace","type":"private"},"date":1695700610,"voice":
                    {"file_id":"VOICE_002", "file_unique_id":"VOICE_UNIQUE_002", "duration":18, "mime_type":"audio/ogg", "file_size":30000}
                }},
                {"update_id":107, "message":{"message_id":207,"from":{"id":108,"is_bot":False,"first_name":"Henry","language_code":"nl"},"chat":{"id":108,"first_name":"Henry","type":"private"},"date":1695700710,"photo":[
                    {"file_id":"PHOTO_567", "file_unique_id":"PHOTO_UNIQUE_567", "file_size":102400, "width":800, "height":600}
                ], "caption": "Throwback to last summer!"}},
                {"update_id":108, "message":{"message_id":208,"from":{"id":109,"is_bot":False,"first_name":"Ivy","language_code":"pt"},"chat":{"id":109,"first_name":"Ivy","type":"private"},"date":1695700810,"sticker":
                    {"file_id":"STICKER_789", "file_unique_id":"STICKER_UNIQUE_789", "width":512, "height":512, "is_animated":False, "thumb":{"file_id":"THUMB_789", "file_unique_id":"THUMB_UNIQUE_789", "file_size":10240, "width":128, "height":128}}
                }},
                {"update_id":109, "message":{"message_id":209,"from":{"id":110,"is_bot":False,"first_name":"Jack","language_code":"pl"},"chat":{"id":110,"first_name":"Jack","type":"private"},"date":1695700910,"document":
                    {"file_id":"DOC_002", "file_unique_id":"DOC_UNIQUE_002", "file_name":"presentation.pptx", "mime_type":"application/vnd.openxmlformats-officedocument.presentationml.presentation", "file_size":409600}
                }}
            ]
        }
        bot = Botto(
            mock_db_connection=sqlite3.connect(':memory:'),
            mock_requests=MockRequest(message_dict),
            mock_token=True
        )

        bot.get_messages()

        expected_messages = [
            Message(chat_id=101, update_id=100, content="Hey, how are you doing?"),
            Message(chat_id=106, update_id=105, content="Just got this new song. What do you think?"),
        ]

        for expected, actual in zip(expected_messages, bot.messages):
            self.assertEqual(expected.chat_id, actual.chat_id)
            self.assertEqual(expected.update_id, actual.update_id)
            self.assertEqual(expected.content, actual.content)



if __name__ == '__main__':
    unittest.main()

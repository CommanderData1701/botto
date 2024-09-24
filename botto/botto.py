from .user import User
from .database import Database
from .message import Message
from .message_handlers import (
    Done,
    SetupHandler,
)

import json
import os
import requests


class Botto:
    def __init__(self, mock_db_connection=None, mock_requests=None):
        try:
            self.load_config()
        except FileNotFoundError:
            self.create_config()
            self.load_config()

        self.database = Database(mock_db_connection)
        self.token: str = os.getenv('BOT_TOKEN')

        if mock_requests:
            self.requests = mock_requests
        else:
            self.requests = requests

        if not self.token:
            raise ValueError('BOT_TOKEN environment variable is not set')

        self.users: list[User] = self.database.get_users()
        self.unregistered_users: list[User] = list()

        self.messages: list[Message] = list()

    def reload(self):
        self.users = self.database.get_users()

    def get_messages(self) -> None:
        if self.last_updated:
            response = self.requests.get(
                f'https://api.telegram.org/bot{self.token}/getUpdates?offset={self.last_updated + 1}'
            )
        else:
            response = self.requests.get(
                f'https://api.telegram.org/bot{self.token}/getUpdates'
            )

        if response.status_code != 200:
            raise RuntimeError(f'Failed to get messages, code {response.status_code}')

        data = response.json()
        if not data['ok']:
            return

        for message in data['result']:
            try:
                chat_id = message['message']['chat']['id']
                date = message['update_id']
                content = message['message']['text']

                self.messages.append(Message(chat_id, date, content))

            except KeyError:
                continue

        if not self.messages:
            return

        self.messages.sort()

        last_updated = self.messages[-1].date

        self.last_updated = last_updated

        self.update_config()

    def handle_message(self):
        if not self.is_configured and len(self.messages) != 0:
            self.users.append(self.database.create_user('root', is_admin=True))
            self.setup()
            self.update_config()

        registered_user_messages = [
            (message, user) 
            for message in self.messages 
            for user in self.users 
            if user.chat_id == message['message']['chat']['id']
        ]

        for message, user in registered_user_messages:
            response = user.handle_message(message['message']['text'])
            if user.handler and user.handler.state == Done.DONE:
                if isinstance(user.handler, SetupHandler):
                    pass

            self.send_message(response, [user])

        self.messages.clear()
            

    def setup(self):
        message = self.messages[0]
        chat_id = message.chat_id
        message_text = message.content

        self.users[0].chat_id = chat_id
        self.users[0].handler = SetupHandler()

        self.database.set_user_chat_id(self.users[0], chat_id)

        response = self.users[0].handler.generate_response(message_text)

        self.send_message(response, [self.users[0]])

    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        self.language = config['language']
        self.is_configured = config['is_configured']
        self.last_updated = config['last_updated']

    def send_message(self, message: str, users: list[User]):
        if not message:
            return

        for user in users:
            id = user.chat_id

            if id:
                response = requests.post(
                    f'https://api.telegram.org/bot{self.token}/sendMessage',
                    json={
                        'chat_id': id,
                        'text': message
                    }
                )

                if response.status_code != 200:
                    raise RuntimeError(f'Message was not sent, code {response.status_code}')

            else:
                raise ValueError('User does not have a chat_id')

    def update_config(self):
        try:
            with open('config.json', 'w') as f:
                json.dump({"is_configured": self.is_configured, "language": self.language, "last_updated": self.last_updated}, f)
        except FileNotFoundError:
            self.create_config()
            self.update_config()

    def create_config(self):
        default_config = {"is_configured": False, "language": "en", "last_updated": None}

        with open('config.json', 'w') as f:
            json.dump(default_config, f)

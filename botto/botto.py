from .user import User
from .database import Database

from .message_handlers import (
    Done,
    SetupHandler,
)

from random import choice
import json
import os
import requests


class Botto:
    def __init__(self):
        try:
            self.load_config()
        except FileNotFoundError:
            self.create_config()
            self.load_config()

        self.database = Database()
        self.token = os.getenv('BOT_TOKEN')

        self.database.create_tables()

        self.users = self.database.get_users()
        self.unregistered_users = list()

        self.messages = list()

    def reload(self):
        self.users = self.database.get_users()

    def get_messages(self) -> None:
        response = requests.get(
            f'https://api.telegram.org/bot{self.token}/getUpdates'
        )

        if response.status_code != 200:
            raise RuntimeError(f'Failed to get messages, code {response.status_code}')

        data = response.json()
        print(data)

        for message in data['result']:
            if message not in self.messages and not self.last_updated:
                self.messages.append(message)
            else:
                self.messages.append(message) if message['message']['date'] > self.last_updated else None

        last_updated = max([message["message"]["date"] for message in self.messages])

        self.last_updated = last_updated

    def handle_message(self):
        if not self.is_configured and len(self.messages) != 0:
            self.users.append(self.database.create_user('root', is_admin=True))
            self.setup()
            self.is_configured = True
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
        chat_id = message['message']['chat']['id']
        message_text = message['message']['text']

        self.users[0].chat_id = chat_id
        self.users[0].handler = SetupHandler()

        print(self.users[0])

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

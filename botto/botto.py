"""
botto.py

This module contains the Botto class, which is the main class of the bot.
"""

import json
import os
from typing import Optional
import logging

import requests

from .user import User
from .database import Database
from .message import Message
from .session import Session
from .message_handlers import (
    Done,
    SetupHandler,
)


class Botto:
    """
    Class represents the botto chatbot client.

    Attributes:
    ----------
    last_updated: Optional[int]
        The last update id of the messages.

    is_configured: bool
        Whether the bot is configured or not.

    database: Database
        The database object.

    requests: requests
        The requests object. Needs to be attribute for mocking in tests.

    token: str
        The token with which the bot client can authenticate itself.

    session: Session
        An object containing session information.

    Methods:
    --------
    reload():
        Reloads the session with the users from the database.

    get_messages():
        Retrieves the messages from the telegram api.

    handle_message():
        Handles the messages from the users, and sends responses.

    setup():
        Sets up the bot for the first time, with the user that writes first.

    load_config():
        Loads the configuration from the config file.

    send_message(message: str, users: list[User]):
        Sends a message to the users in the provided list.

    update_config():
        Updates the configuration file.

    create_config():
        Creates a new configuration if it does not yet exist.
    """
    def __init__(
            self, mock_db_connection=None, mock_requests=None, mock_token=False
    ):
        self.last_updated: Optional[int] = None
        self.is_configured: bool = False
        try:
            self.load_config()
        except FileNotFoundError:
            self.create_config()
            self.load_config()

        self.database = Database(mock_db_connection)

        self.requests = requests if not mock_requests else mock_requests
        self.token = "ABCDEFGHIJKLMNOPQRSTUVWXZY1234567890" if mock_token \
            else os.getenv('BOT_TOKEN')

        if not self.token:
            raise ValueError('BOT_TOKEN environment variable is not set')

        self.session = Session(
            users = self.database.get_users(),
            inactive_users = [],
            messages = []
        )

    def reload(self):
        """
        Reloads the session with the users from the database.
        """
        self.session.users = self.database.get_users()

    def get_messages(self) -> None:
        """
        Retrieves the messages from the telegram api, and stores them in the
        session object.
        """
        if self.last_updated:
            response = self.requests.get(
                f'https://api.telegram.org/bot{self.token}/getUpdates?' \
                + 'offset={self.last_updated + 1}',
                timeout=5
            )
        else:
            response = self.requests.get(
                f'https://api.telegram.org/bot{self.token}/getUpdates',
                timeout=5,
            )

        if response.status_code != 200:
            raise RuntimeError(
                f'Failed to get messages, code {response.status_code}'
            )

        data = response.json()
        if not data['ok']:
            return

        for message in data['result']:
            try:
                chat_id = message['message']['chat']['id']
                update_id = message['update_id']
                content = message['message']['text']

                self.session.messages.append(
                    Message(
                        chat_id=chat_id, update_id=update_id, content=content
                    )
                )

            except KeyError:
                continue

        if not self.session.messages:
            return

        self.session.messages.sort()

        last_updated = self.session.messages[-1].update_id

        self.last_updated = last_updated

        self.update_config()

    def handle_message(self) -> None:
        """
        Handles the messages from the users, and sends responses.
        """
        if not self.is_configured and len(self.session.messages) != 0:
            self.session.users.append(
                self.database.create_user('root', is_admin=True)
            )
            self.setup()
            self.update_config()

        chat_ids = [user.chat_id for user in self.session.users]

        registered_user_messages = [
            message
            for message in self.session.messages
            if message.chat_id in chat_ids
        ]

        for message in registered_user_messages:
            user = [user for user in self.session.users
                if user.chat_id == message.chat_id][0]
            response = user.handle_message(message.content)
            if user.handler and user.handler.get_state() == Done.DONE:
                self.send_message(response, [user])
                if isinstance(user.handler, SetupHandler):
                    data_dict = user.handler()

                    self.database.update_user_name(
                        "root", data_dict["root_name"]
                    )

                    for user_name in data_dict["roommates"]:
                        self.session.users.append(
                            self.database.create_user(user_name)
                        )

                    message = "Here you go! All users and their tokens:\n\n" \
                    + "\n".join(
                        [f"{user.name}: {user.token}"
                                for user in self.session.users]
                    )
                    message += "\nThey just need to provide them when writing" \
                        + " to me and they can get started!"
                    user.handler = None
                    self.send_message(message, [user])
                    self.is_configured = True
                    self.update_config()
                return

            self.send_message(response, [user])

        self.session.messages.clear()

    def setup(self) -> None:
        """
        Setup the bot for the first time, with the user that writes first.
        """
        message = self.session.messages[0]
        chat_id = message.chat_id
        message_text = message.content

        self.session.users[0].chat_id = chat_id
        self.session.users[0].handler = SetupHandler()

        self.database.set_user_chat_id(self.session.users[0], chat_id)

        response = self.session.users[0].handler.generate_response(message_text)

        self.send_message(response, [self.session.users[0]])

    def load_config(self) -> None:
        """
        Loads the configuration from the config file.
        """
        with open('config.json', 'r', encoding="utf-8") as f:
            config = json.load(f)

        self.language = config['language']
        self.is_configured = config['is_configured']
        self.last_updated = config['last_updated']

    def send_message(self, message: str, users: list[User]) -> None:
        """
        Sends a message to the users in the provided list.

        Parameters:
        -----------
        message: str
            The message to send to the users.

        users: list[User]
            The users to send the message to.
        """
        if not message:
            return

        for user in users:
            if user.chat_id:
                response = self.requests.post(
                    f'https://api.telegram.org/bot{self.token}/sendMessage',
                    json={
                        'chat_id': user.chat_id,
                        'text': message
                    },
                    timeout=5
                )

                if response.status_code != 200:
                    raise RuntimeError(
                        f'Message was not sent, code {response.status_code}'
                    )

            else:
                logging.error('User %s has no chat id', user.name)
                return

    def update_config(self) -> None:
        """
        Updates the configuration file.
        """
        try:
            with open('config.json', 'w', encoding="utf-8") as f:
                json.dump(
                    {"is_configured": self.is_configured,
                     "language": self.language,
                     "last_updated": self.last_updated
                     },f)
        except FileNotFoundError:
            logging.info('Generating new config file.')
            self.create_config()
            self.update_config()

    def create_config(self):
        """
        Creates a new configuration if it does not yet exist
        """
        default_config = {
            "is_configured": False, "language": "en", "last_updated": None
        }

        with open('config.json', 'w', encoding="utf-8") as f:
            json.dump(default_config, f)

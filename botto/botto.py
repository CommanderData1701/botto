# -*- coding: utf-8 -*-
"""Module containing the Botto class"""
import json
import os
from typing import Optional
import logging
import sys

import requests # type: ignore

from .user import User
from .database import Database
from .message import Message
from .config import Config
from .message_handlers import (
    DONE,
    SetupHandler,
)
from .mocks import MockObject # type: ignore


class Botto:
    """Main class for the bot.

    The Botto class is the main class for the bot. It connects the messages 
    received from the telegram api with the users and their responses. It also
    stores the data accumulated during the conversation persistently in the 
    database and saves information necessary after a client restart in the 
    config file.

    Attributes:
        config (Config): Object containing config information.
        mock (MockObject): Object containing mock objects for testing.
        requests (requests): Object containing the requests module or mocks.
        database (Database): Object containing the database connection.
        token (str): The token for the telegram bot.
        session (Session): Object containing current session information.
        config_file `static` (str): The name of the config file.
    """
    config_file = 'config.json'

    def __init__(
        self,
        mock: Optional[MockObject] = None,
    ) -> None:
        self.config: Config = Config()
        try:
            self.load_config()
        except FileNotFoundError:
            self.create_config()
            self.load_config()

        self.mock = mock

        self.requests = requests if mock is None else mock.requests
        self.database = Database() if mock is None else \
            Database(mock.db_connection)
        self.token = os.getenv('BOT_TOKEN') if mock is None else \
            'ABCDEFG'
        Botto.config_file = mock.config_file if mock is not None else \
            Botto.config_file

        if not self.token:
            logging.error('No token found in environment variables.')
            print('No token found in environment variables.')
            sys.exit(1)

        self.active_users: list[User] = []

    def get_messages(self) -> None:
        """Retrieves the messages from telegram bot api.
        
        Messages are stored as Message objects in the session object.
        """
        if self.config.last_updated:
            response = self.requests.get(
                f'https://api.telegram.org/bot{self.token}/getUpdates?' \
                + f'offset={self.config.last_updated + 1}',
                timeout=5
            )
        else:
            response = self.requests.get(
                f'https://api.telegram.org/bot{self.token}/getUpdates',
                timeout=5,
            )

        match response.status_code:
            case 200:
                pass
            case 404:
                logging.error('Messages could not be retrieved. Maybe the ' \
                              + 'token is invalid.')
                return
            case _:
                logging.error('Messages could not be retrieved. Status code: ' \
                              + '%d', response.status_code)
                return

        data = response.json()
        if data is None or not data['ok']:
            logging.error('No messages retrieved or data is not in json format')
            return

        users = self.database.get_users()

        for message in data['result']:
            try:
                chat_id = message['message']['chat']['id']
                update_id = message['update_id']
                content = message['message']['text']
                
                user_present = [user for user in users if user == chat_id]


            except KeyError:
                continue

        if not self.session.messages:
            return

        self.session.messages.sort()

        last_updated = self.session.messages[-1].update_id

        self.config.last_updated = last_updated

        self.update_config()

    def handle_message(self) -> None:
        """Handles current session messages and deletes them afterwards."""
        if not self.config.is_configured and len(self.session.users) == 0 \
            and len(self.session.messages) != 0:
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
            if user.handler and user.handler.get_state() == DONE:
                self.send_message(response, [user])
                if isinstance(user.handler, SetupHandler):
                    data_dict = user.handler()
                    new_root_name = str(data_dict["root_name"])

                    self.database.update_user_name(
                        "root", new_root_name
                    )
                    self.session.users[0].name = new_root_name

                    for user_name in data_dict["roommates"]:
                        self.session.users.append(
                            self.database.create_user(user_name)
                        )

                    message_text = "Here you go! All users and their tokens:" \
                        + "\n\n" + "\n".join(
                        [f"{user.name}: {user.token}"
                                for user in self.session.users]
                    )
                    message_text += "\n\nThey just need to provide them when" \
                        + " writing to me and they can get started!"
                    user.handler = None
                    self.send_message(message_text, [user])
                    self.config.is_configured = True
                    self.update_config()
                return

            self.send_message(response, [user])

        self.session.messages.clear()

    def setup(self) -> None:
        """Set root user as first person to write to the bot."""
        message = self.session.messages[0]
        chat_id = message.chat_id

        self.session.users[0].chat_id = chat_id
        self.session.users[0].handler = SetupHandler()

        self.database.set_user_chat_id(self.session.users[0], chat_id)

    def load_config(self) -> None:
        """Loads the Config object from the config file."""
        with open(Botto.config_file, 'r', encoding="utf-8") as f:
            config = json.load(f)

        self.language = config['language']
        self.config.is_configured = config['is_configured']
        self.config.last_updated = config['last_updated']

    def send_message(self, message: str, users: list[User]) -> None:
        """Sends message to a list of users.
        
        Args:
            message (str): The message to be sent.
            users (list[User]): The users to send the message to.
        """
        if not message:
            return

        for user in users:
            if user.chat_id is not None:
                response = self.requests.post(
                    f'https://api.telegram.org/bot{self.token}/sendMessage',
                    json={
                        'chat_id': user.chat_id,
                        'text': message
                    },
                    timeout=5
                )

                match response.status_code:
                    case 200:
                        pass
                    case 404:
                        logging.error('Message was not sent. Maybe the chat' \
                                    + ' id is invalid.')
                        return
                    case _:
                        logging.error('Message was not sent, status code: %d',
                                    response.status_code)
                        return

            else:
                logging.error('User %s has no chat id', user.name)
                return

    def update_config(self) -> None:
        """Updates the configuration file.

        The configuration file is updated with the current configuration. If the
        file is not found it is created.
        """
        try:
            with open(Botto.config_file, 'w', encoding="utf-8") as f:
                json.dump(
                    {"is_configured": self.config.is_configured,
                     "language": self.language,
                     "last_updated": self.config.last_updated
                     },f)
        except FileNotFoundError:
            logging.info('Generating new config file.')
            self.create_config()
            self.update_config()

    def create_config(self) -> None:
        """Creates a new configuration if it does not yet exist

        The configuration file is created with the default configuration if it
        does not yet exist.

        Example:
            The default configuration is:
            {
                "is_configured": False,
                "language": "en",
                "last_updated": None
            }
        """
        default_config = {
            "is_configured": False, "language": "en", "last_updated": None
        }

        with open(Botto.config_file, 'w', encoding="utf-8") as f:
            json.dump(default_config, f)

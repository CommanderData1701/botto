# -*- coding: utf-8 -*-
"""Module for the User class."""
from dataclasses import dataclass
from typing import Optional

from botto.message_handlers import Handler
from botto.message import Message


@dataclass
class User:
    """Class representing a user of the bot.

    Attributes:
        name (str): The name of the user.
        chat_id (Optional[int]): The chat id of the user.
        is_admin (bool): A flag to indicate if the user is an admin.
        token (Optional[str]): The token of the user.
        handler (Optional[Handler]): The handler the user is currently in.

    Todo:
        * Implement the set_handler method.
    """
    name: Optional[str] = None
    chat_id: Optional[int] = None
    is_admin: bool = False
    token: Optional[str] = None
    handler: Optional[Handler] = None
    message: Optional[Message] = None

    def set_handler(self) -> None:
        pass

    def __str__(self) -> str:
        """Returns a string representation of the user.

        Returns:
            str: The string representation of the user.
                (e.g. User(name=John, chat_id=123456, is_admin=True)
        """
        return f"User(name={self.name}, chat_id={self.chat_id}," + \
            f" is_admin={self.is_admin})"

    def __hash__(self) -> int:
        """Hashes the user by the name."""
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        """Compares the user to another user, a string or an int.

        Parameters:
            other (object): The object to compare with.

        Returns:
            bool: True if other is of type User and the names are equal. If
                other is of type str the names are compared. If other is of type
                int the chat_id is compared.
        """
        if isinstance(other, User):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, int):
            return self.chat_id == other

        return False

    def handle_message(self) -> str:
        """Handles a message from the user.

        Hanldes messages either according to the handler, or as a command 
        entering a conversation.

        Parameters:
            message (str): The message to handle.

        Returns:
            str: The response to the message.

        Raises:
            RuntimeError: If the message is None.
        """
        if self.message == "/exit" and self.handler is not None:
            self.handler = None
            return "Exited"
        if self.handler:
            return self.handler.generate_response(self.message.content)

        match self.message:
            case "/help":
                return self.help()
            case _:
                return "That is not a valid command. Type /help for a list of" \
                    + " commands."

    def help(self) -> str:
        """Returns a help message according to the user's admin status.

        Returns:
            str: The help message.
        """
        message = """
        /help - Display this message
        /exit - Exit current operation
        /shopping_list - Display shopping list
        /add_item - Add item to shopping list
        /disaster - Something is untidy? Complain by calling a disaster.
        """

        admin_commands = "" if self.is_admin else """

        /setup_cleaning - Set up cleaning schedule
        /change_username - Change users name
        /remove_user - Remove user
        /add_user - Add user
        """

        return message + admin_commands

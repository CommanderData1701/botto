"""
Contains user class to handle business logic for the botto chatbot client users.
"""
from dataclasses import dataclass
from typing import Optional

from .message_handlers import (
        Handler,
)


@dataclass
class User:
    """
    Class represents the user of the botto chatbot client.

    Attributes:
    ----------
    name: str
        The name of the user.

    chat_id: Optional[int]
        The chat id within the telegram chatbot api

    is_admin: bool
        Whether the user is an admin or not.

    token: Optional[str]
        The token which a user can use to authenticate themselves.

    handler: Optional[Handler]
        The handler which is used to handle messages from the user.


    Methods:
    --------
    __str__():
        Returns a string representation of the user.

    __hash__():
        Hashes the user according to their name.

    __eq__(other):
        Compares the user to another user by their name.

    handle_message(message: str) -> str:
        Handles a message from the user and provides the response.

    help():
        Returns a help message for the user.
    """
    name: str
    chat_id: Optional[int] = None
    is_admin: bool = False
    token: Optional[str] = None
    handler: Optional[Handler] = None

    def __str__(self):
        return f"User(name={self.name}, chat_id={self.chat_id}," \
            + " is_admin={self.is_admin})"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def handle_message(self, message: str) -> str:
        """
        Handles a message from the user and provides the response.

        Parameters:
        -----------
        message: str
            The message from the user.

        Returns:
        --------
        str:
            The response to the message.
        """
        if message == "/exit":
            self.handler = None
            return "Exited"
        if self.handler:
            return self.handler.generate_response(message)

        match message:
            case "/help":
                return self.help()
            case _:
                return "That is not a valid command. Type /help for a list of" \
                    + " commands."

    def help(self):
        """
        Returns a help message for the user.

        Returns:
        --------
        str:
            The help message.
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

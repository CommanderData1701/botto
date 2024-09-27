from dataclasses import dataclass
from typing import Optional

from .message_handlers import (
        Handler,
)


@dataclass
class User:
    name: str
    chat_id: Optional[int] = None
    is_admin: bool = False
    token: Optional[str] = None
    handler: Optional[Handler] = None

    def __str__(self):
        return f"User(name={self.name}, chat_id={self.chat_id}, is_admin={self.is_admin})"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def handle_message(self, message: str) -> str:
        if message == "/exit":
            self.handler = None
            return "Exited"
        elif self.handler:
            return self.handler.generate_response(message)
        else:
            match message:
                case "/help":
                    return self.help()
                case _:
                    return "That is not a valid command. Type /help for a list of commands."


    def help(self):
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

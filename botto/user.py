from .message_handlers import (
        Handler,
)

from dataclasses import dataclass


@dataclass
class User:
    name: str
    chat_id: int = None
    is_admin: bool = False
    handler: Handler = None

    def __str__(self):
        return f"User(name={self.name}, chat_id={self.chat_id}, is_admin={self.is_admin})"

    def __hash__(self):
        return hash(self.chat_id)

    def __eq__(self, other):
        return self.chat_id == other.chat_id

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
        """

        admin_commands = "" if self.is_admin else """
        /setup_cleaning - Set up cleaning schedule
        /change_username - Change users name
        """

        return message + admin_commands

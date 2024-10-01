# -*- coding: utf-8 -*-
"""Contains the handler class for setup converstion."""
from enum import Enum
from typing import Union, Any
from typing_extensions import override

from .message_handler_base import Handler
from .done_enum import DONE, Done


class SetupHandler(Handler):
    """SetupHandler class that handles the setup process of the bot.

    Class handles the setup process of the bot. It returns the root user's name
    and the names of the roommates as information once the converstion has 
    terminated. It is only created for the first message of a user writing to 
    the bot, that user is the root.
    """
    class State(Enum):
        """Enum class that represents the states of the setup conversation.

        Attributes:
            BEGIN: Represents the start of the conversation. State is assigned
                at construction of the handler.
            CONFIRM_NAME: Asks the root user to confirm their name.
            CHANGE_NAME: Asks the root user to provide their name again if it 
                was not entered correctly the first time.
            SET_UP_USERS: Asks the root user to provide the names of root user's
                flatmates.
            CONFIRM_USERS: Asks the root user to confirm the names of the 
                entered flatmate names.
            CHANGE_USERS: Asks the root user to provide the names of the
                flatmates again if they were not entered correctly the first
                time.
        """
        BEGIN = "Hello! You are now the root user. What's your name?"
        CONFIRM_NAME = "Hello, {name}! Is this correct? (yes/no)"
        CHANGE_NAME = "Ok, what is it then?"
        SET_UP_USERS = "Great! Now tell us who your roommates are. (Seperated" \
            + " by commas)"
        CONFIRM_USERS = "Are {users} your roommates? (yes/no)"
        CHANGE_USERS = "Ok, who are they then?"

    def __init__(self) -> None:
        self.state: Union[SetupHandler.State, Done] = self.State.BEGIN
        self.root_name: str = "root"
        self.users: list[str] = []

    @override
    def __call__(self) -> dict[str, Any]:
        if self.state != DONE:
            raise ValueError("Handler is not done yet")

        return {"root_name": self.root_name, "roommates": self.users}

    @override
    def get_state(self) -> Enum:
        return self.state

    @override
    def generate_response(self, message: str) -> str:
        response: str = self.state.value

        match self.state:
            case self.State.BEGIN:
                self.state = self.State.CONFIRM_NAME

            case self.State.CONFIRM_NAME:
                self.root_name = message.strip()
                self.state = self.State.CHANGE_NAME
                response = response.format(name=self.root_name)

            case self.State.CHANGE_NAME:
                if message.lower() == "yes":
                    self.state = self.State.SET_UP_USERS
                    response = self.State.SET_UP_USERS.value
                elif message.lower() == "no":
                    self.state = self.State.CONFIRM_NAME
                else:
                    response = "Answer must be 'yes' or 'no'"

            case self.State.SET_UP_USERS:
                self.users = message.split(",")
                self.users = [user.strip() for user in self.users]
                checklist = self.users.copy()
                checklist.append(self.root_name)

                if len(checklist) != len(set(checklist)):
                    response = "There are douplicates in the users. Please" \
                    + " provide a unique list of users."
                else:
                    self.state = self.State.CONFIRM_USERS
                    user_string = ", ".join(self.users)
                    response = self.State.CONFIRM_USERS.value.format(
                        users=user_string
                    )

            case self.State.CONFIRM_USERS:
                if message.lower() == "yes":
                    self.state = DONE
                    response = DONE.value
                elif message.lower() == "no":
                    self.state = self.State.SET_UP_USERS
                    response = self.State.CHANGE_USERS.value
                else:
                    response = "Answer must be 'yes' or 'no'"

        return response

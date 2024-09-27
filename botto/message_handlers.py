"""
message_handlers.py

Contains Handler classes to handle messages from users and generate responses.

Classes:
--------
Done:
    Enum class that contains the value "DONE" to indicate that the setup process
    is done.

Handler:
    Abstract class that defines the structure of a handler. All classes within
    this module should inherit from this class.

SetupHandler:
    Class that handles the setup process of the bot.
"""

from typing import Optional

from enum import Enum


class Done(Enum):
    """
    Enum class that contains the value "DONE" to indicate that the setup process
    is done. This needs to be accessible outside of the Handler classes.

    Attributes:
    ----------
    DONE : str
        The value that indicates that the setup process is done.
    """

    DONE = "All set!"


class Handler:
    """
    Abstract class that defines the structure of a handler. All classes within
    this module should inherit from this class.

    Methods:
    --------
    generate_response:
        Abstract method that generates a response based on the message received.

    __call__:
        Provide additional information that the handler generated during the
        conversation.
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def generate_response(self, message: str) -> Optional[str]:
        """
        Generates a response based on the message received.

        Parameters:
        -----------
        message : str
            The message received from the user.

        Returns:
        --------
        str
            The response generated based on the message received.
        """
        raise NotImplementedError

    def __call__(self) -> dict[str, str]:
        """
        Provide additional information that the handler generated during the
        conversation.

        Returns:
        --------
        dict
            The additional information generated during the conversation.
        """
        raise NotImplementedError


class SetupHandler(Handler):
    """
    Class that handles the setup process of the bot.


    Classes:
    --------
    State:
        Enum class that contains the different states of the setup process.

    Attributes:
    ----------
    root_name : str
        The name of the root user.

    state : State
        The current state of the setup process.

    users : list[str]
        The names of the roommates.

    Methods:
    --------
    generate_response:
        Generates a response based on the message received.
    """

    class State(Enum):
        """
        Enum class that contains the different states of the setup process.

        Attributes:
        ----------
        BEGIN : str
            The message that asks the user for their name.

        CONFIRM_NAME : lambda name: str
            The message that confirms the name of the user.

        CHANGE_NAME : str
            The message that asks the user to change their name.

        SET_UP_USERS : str
            The message that asks the user for the names of their roommates.

        CONFIRM_USERS : lambda users: str
            The message that confirms the names of the roommates.

        CHANGE_USERS : str
            The message that asks the user to change the names of the roommates.
        """
        BEGIN = "Hello! You are now the root user. What's your name?"
        CONFIRM_NAME = "Hello, {name}! Is this correct? (yes/no)"
        CHANGE_NAME = "Ok, what is it then?"
        SET_UP_USERS = "Great! Now tell us who your roommates are. (Seperated \
            by commas)"
        CONFIRM_USERS = "Are {users} your roommates? (yes/no)"
        CHANGE_USERS = "Ok, who are they then?"

    def __init__(self) -> None:
        self.state = self.State.BEGIN
        self.root_name = ""
        self.users = []

    def __call__(self) -> dict:
        if self.state != Done.DONE:
            raise ValueError("Handler is not done yet")

        return {"root_name": self.root_name, "roommates": self.users}

    def generate_response(self, message: str) -> Optional[str]:
        match self.state:
            case self.State.BEGIN:
                self.state = self.State.CONFIRM_NAME
                return self.State.BEGIN.value

            case self.State.CONFIRM_NAME:
                self.root_name = message.strip()
                self.state = self.State.CHANGE_NAME
                return self.State.CONFIRM_NAME.value.format(name=self.root_name)

            case self.State.CHANGE_NAME:
                if message.lower() == "yes":
                    self.state = self.State.SET_UP_USERS
                    return self.State.SET_UP_USERS.value
                if message.lower() == "no":
                    self.state = self.State.CONFIRM_NAME
                    return self.State.CHANGE_NAME.value
                else:
                    return "Answer must be 'yes' or 'no'"

            case self.State.SET_UP_USERS:
                self.users = message.split(",")
                self.users = [user.strip() for user in self.users]
                checklist = self.users.copy()
                checklist.append(self.root_name)

                if len(checklist) != len(set(checklist)):
                    return "There are douplicates in the users. Please provide \
                    a unique list of users."

                self.state = self.State.CONFIRM_USERS
                user_string = ", ".join(self.users)
                return self.State.CONFIRM_USERS.value.format(user_string)

            case self.State.CONFIRM_USERS:
                if message.lower() == "yes":
                    self.state = Done.DONE
                    return Done.DONE.value
                if message.lower() == "no":
                    self.state = self.State.SET_UP_USERS
                    return self.State.CHANGE_USERS.value
                else:
                    return "Answer must be 'yes' or 'no'"

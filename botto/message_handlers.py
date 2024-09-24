from enum import Enum
from typing import Union


class Done(Enum):
    DONE = "All set!"


class Handler:
    def __init__(self) -> None:
        raise NotImplementedError

    def generate_response(self, message: str) -> str:
        raise NotImplementedError

    def __call__(self) -> dict[str, str]:
        raise NotImplementedError


class SetupHandler(Handler):
    class State(Enum):
        BEGIN = "Hello! You are now the root user. What's your name?"
        CONFIRM_NAME = lambda name: f"Hello, {name}! Is this correct? (yes/no)"
        CHANGE_NAME = "Ok, what is it then?"
        SET_UP_USERS = f"Great! Now tell us who your roommates are. (Seperated by commas)"
        CONFIRM_USERS = lambda users: f"Are {users} your roommates? (yes/no)"
        CHANGE_USERS = "Ok, who are they then?"

    def __init__(self) -> None:
        self.state = self.State.BEGIN

    def __call__(self) -> dict:
        if self.state != Done.DONE:
            raise ValueError("Handler is not done yet")

        return {"root_name": self.root_name, "roommates": self.users}

    def generate_response(self, message: str) -> str:
        match self.state:
            case self.State.BEGIN:
                self.state = self.State.CONFIRM_NAME
                return self.State.BEGIN.value

            case self.State.CONFIRM_NAME:
                self.root_name = message.strip()
                self.state = self.State.CHANGE_NAME
                return self.State.CONFIRM_NAME(self.root_name)

            case self.State.CHANGE_NAME:
                if message.lower() == "yes":
                    self.state = self.State.SET_UP_USERS
                    return self.State.SET_UP_USERS.value
                elif message.lower() == "no":
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
                    return "There are douplicates in the users. Please provide a unique list of users."

                self.state = self.State.CONFIRM_USERS
                user_string = ", ".join(self.users)
                return self.State.CONFIRM_USERS(user_string)

            case self.State.CONFIRM_USERS:
                if message.lower() == "yes":
                    self.state = Done.DONE
                    return Done.DONE.value
                elif message.lower() == "no":
                    self.state = self.State.SET_UP_USERS
                    return self.State.CHANGE_USERS.value
                else:
                    return "Answer must be 'yes' or 'no'"


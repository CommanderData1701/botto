from enum import Enum


class Done(Enum):
    DONE = "All set!"


class Handler:
    def __init__(self):
        raise NotImplementedError

    def generate_response(self, message: str) -> str:
        raise NotImplementedError

    def __call__(self):
        raise NotImplementedError


class SetupHandler(Handler):
    class State(Enum):
        BEGIN = "Hello! You are now the root user. What's your name?"
        CONFIRM_NAME = lambda name: f"Hello, {name}! Is this correct? (yes/no)"
        CHANGE_NAME = "Ok, what is it then?"
        SET_UP_USERS = f"Great! Now tell us who your roommates are. (Seperated by commas)"
        CONFIRM_USERS = lambda users: f"""Are these the correct roommates? 
        {users} (yes/no)"""
        CHANGE_USERS = "Ok, who are they then?"

    def __init__(self):
        self.state = self.State.BEGIN

    def generate_response(self, message: str) -> str:
        match self.state:
            case self.State.BEGIN:
                self.state = self.State.CONFIRM_NAME
                self.root_name = message
                return self.State.BEGIN.value

            case self.State.CONFIRM_NAME:
                self.state = self.State.CHANGE_NAME
                return self.State.CONFIRM_NAME(message)

            case self.State.CHANGE_NAME:
                if message.lower() == "yes":
                    self.state = self.State.SET_UP_USERS
                    return self.State.SET_UP_USERS.value
                elif message.lower() == "no":
                    self.state = self.State.CONFIRM_NAME
                    return self.State.CHANGE_NAME
                else:
                    return "Answer must be 'yes' or 'no'"

            case self.State.SET_UP_USERS:
                self.state = next(self.state)
                return self.State.SET_UP_USERS.value

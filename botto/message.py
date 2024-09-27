"""
message.py

Only contains the Message class.
"""
from dataclasses import dataclass

from .user import User


@dataclass
class Message:
    """
    Class that represents a message sent by a user.

    Attributes:
    ----------
    chat_id : int
        The id of the chat where the message was sent.

    update_id : int
        The id of the message. Is a representation of the time the message was 
        sent.

    content : str
        The content of the message.
    """
    chat_id: int
    update_id: int
    content: str

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.update_id == other
        if isinstance(other, str):
            return self.content == other
        if isinstance(other, User):
            return self.chat_id == other.chat_id
        if isinstance(other, Message):
            return self.update_id == other.update_id

        return False

    def __gt__(self, other: "Message") -> bool:
        return self.update_id > other.update_id

    def __lt__(self, other: "Message") -> bool:
        return self.update_id < other.update_id

    def __ge__(self, other: "Message") -> bool:
        return self.update_id >= other.update_id

    def __le__(self, other: "Message") -> bool:
        return self.update_id <= other.update_id

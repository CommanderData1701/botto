# -*- coding: utf-8 -*-
"""Module containing the Message class."""
from dataclasses import dataclass

from .user import User


@dataclass
class Message:
    """Class that represents a message.

    Attributes:
        chat_id (int): The chat id of the message.
        update_id (int): The update id of the message.
        content (str): The content of the message.
    """
    chat_id: int
    update_id: int
    content: str

    def __eq__(self, other: object) -> bool:
        """Compares all Message object to int, str, Message or User.
        
        Parameters:
            other (object): The object to compare with.
        
        Returns:
            bool: True if other is of type Message and update_ids are equal.
                If other is of type int the update_id is compared. If other is
                of type str the content is compared. If other is of type User
                the chat_id is compared.
        """
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
        """Compares the update_id of two Message objects."""
        return self.update_id > other.update_id

    def __lt__(self, other: "Message") -> bool:
        """Compares the update_id of two Message objects."""
        return self.update_id < other.update_id

    def __ge__(self, other: "Message") -> bool:
        """Compares the update_id of two Message objects."""
        return self.update_id >= other.update_id

    def __le__(self, other: "Message") -> bool:
        """Compares the update_id of two Message objects."""
        return self.update_id <= other.update_id

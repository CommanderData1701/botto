"""
session.py

This module contains the Session class, which is used to manage the user's 
session.
"""

from dataclasses import dataclass

from .user import User
from .message import Message


@dataclass
class Session:
    """
    Class represents the session of the botto chatbot client.

    Attributes:
    ----------
    users: list[User]
        The list of users in the session.

    inactive_users: list[User]
        The list of inactive users in the session.

    messages: list[Message]
        The list of current messages in the session.
    """
    users: list[User]
    inactive_users: list[User]
    messages: list[Message]

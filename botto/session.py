# -*- coding: utf-8 -*-
"""Module for the Session class."""
from dataclasses import dataclass

from .user import User
from .message import Message


@dataclass
class Session:
    """Class representing necessary session information of the bot.

    Attributes:
        users (list[User]): List of users in the session.
        inactive_users (list[User]): List of inactive users in the session.
        messages (list[Message]): List of messages in the session.
    """
    users: list[User]
    inactive_users: list[User]
    messages: list[Message]

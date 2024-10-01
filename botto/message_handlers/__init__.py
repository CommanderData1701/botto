# -*- coding: utf-8 -*-
"""Module containing all message handlers.

Message handlers are desinged to handle states of a conversation, and to change
that stage based on the input received and generate an appropriate response. 
Each handler should inherit from the Handler class in message_handler_base.py
with the state being represented by an Enum class within the respective Handler.

Attributes:
    DONE (Enum): Enum class that contains the single value "DONE" to indicate 
        that the converstion of a handler has terminated.

Example:
    The SetupHandler class in setup_handler.py is an example of a message 
    handler. It handles the first conversation the bot starts with a user to 
    set up the bot with the shared flat information.
"""

__all__ = [
    "SetupHandler",
    "DONE",
]

from .setup_handler import SetupHandler
from .done_enum import DONE

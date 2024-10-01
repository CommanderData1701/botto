# -*- coding: utf-8 -*-
"""Base class for all message handlers."""
from enum import Enum
from typing import Any


class Handler:
    """Base class for all message handlers.

    This class should be inherited by all message handlers. It provides the
    basic structure that all handlers should follow.
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def get_state(self) -> Enum:
        """Returns the current state of the handler.

        Returns:
            Enum: The current state of the handler.
        """
        raise NotImplementedError

    def generate_response(self, message: str) -> str:
        """Generates a response based on the message received.

        Every handler should return a response according to an input message.

        Args:
            message (str): The message received by the handler.

        Returns:
            str: The response generated by the handler.
        """
        raise NotImplementedError

    def __call__(self) -> dict[str, Any]:
        """Returns the additional information gathered by the handler.

        This method should return a dictionary containing the additional 
        information leading to the systems state change.

        Returns:
            dict[str, Any]: A dictionary containing the additional information
                gathered by the handler. Value type is not defined.
        """
        raise NotImplementedError

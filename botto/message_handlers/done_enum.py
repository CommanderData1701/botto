# -*- coding: utf-8 -*-
"""Contains the global termination state for handlers."""
from enum import Enum


class Done(Enum):
    """Global termination state for handlers.

    Enum class that contains the value "DONE" to indicate that the setup process
    is done. This needs to be accessible outside of the Handler classes.

    Attributes:
        DONE: The value that indicates that the setup process is done.
    """
    DONE = "All set!"


"""Exported as single variable"""
DONE = Done.DONE

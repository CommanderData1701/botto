# -*- coding: utf-8 -*-
"""Module containing the Config class."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Class representing config information of the bot.

    The Config class is a dataclass that holds the configuration information of
    the bot.

    Attributes:
        last_updated (Optional[int]): The id of the last update pulled from the
            telegram api.
        is_configured (bool): A flag to indicate if the bot is configured.
    """
    last_updated: Optional[int] = None
    is_configured: bool = False

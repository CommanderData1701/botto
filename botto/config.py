"""
config.py

This module contains a dataclass concerned with config information of the bot.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """
    Class represents the configuration of the bot.

    Attributes:
    ----------
    last_updated: int
        The last update id of the messages.

    is_configured: bool
        Whether the bot is configured or not.
    """
    last_updated: Optional[int] = None
    is_configured: bool = False

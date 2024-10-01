# -*- coding: utf-8 -*-
"""Main module of the botto chatbot client.

This module contains the main function that starts the bot and runs it. It 
requires the bot token as an evnironment variable, otherwise it will exit with
an error.

Example:
    To run the bot, simply execute the main function.

        $ export BOT_TOKEN=<your-bot-token> python main.py

    It is recommended to use the docker image provided.

Attributes:
    LOGFILE (str): The path to the log file. It is created on the fly and logs
        all messages and errors that the bot receives and sends.
"""
from datetime import datetime
from pathlib import Path
from os import mkdir
import logging

from botto import Botto

if not Path('logs').exists():
    mkdir('logs')

LOGFILE = f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
logging.basicConfig(
    filename=LOGFILE,
    level=logging.DEBUG,
    format='[%(asctime)s - %(name)s - %(levelname)s] - %(message)s'
)


def main() -> None:
    bot = Botto()

    while True:
        bot.get_messages()
        bot.handle_message()


if __name__ == "__main__":
    main()

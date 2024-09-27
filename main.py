"""
This serves as the main file for the botto chatbot client. It requires
the bot token as an environment variable.
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
    """
    Main function for the botto chatbot client.

    Args:
        None

    Returns:
        None

    Raises:
        RuntimeError: If the BOT_TOKEN environment variable is not set.
    """
    bot = Botto()

    while True:
        try:
            bot.get_messages()
        except Exception as e:
            print(e)
        bot.handle_message()


if __name__ == "__main__":
    main()

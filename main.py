from botto import Botto
from datetime import datetime
from pathlib import Path
from os import mkdir
import logging

if not Path('logs').exists():
    mkdir('logs')

filename = f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
logging.basicConfig(
    filename=filename,
    level=logging.DEBUG,
    format='[%(asctime)s - %(name)s - %(levelname)s] - %(message)s'
)


def main() -> None:
    bot = Botto()

    while True:
        try:
            bot.get_messages()
        except Exception as e:
            print(e)
        bot.handle_message()


if __name__ == "__main__":
    main()

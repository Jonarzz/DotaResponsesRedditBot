"""Module to run the bot. Executes the work() method of bot that executes the endless loop of reading comments and
submissions and replying to them if the match any response.
"""
from bot.worker import work, logger
from util.logger import setup_logger

__author__ = 'MePsyDuck'

if __name__ == '__main__':
    setup_logger()
    try:
        work()
    except (KeyboardInterrupt, SystemExit):
        logger.exception("Script stopped")

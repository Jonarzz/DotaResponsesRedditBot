from bot.worker import work, logger
from util.logger import setup_logger

__author__ = 'MePsyDuck'

if __name__ == '__main__':
    setup_logger()
    try:
        work()
    except (KeyboardInterrupt, SystemExit):
        logger.exception("Script stopped")

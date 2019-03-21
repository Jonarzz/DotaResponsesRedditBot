import traceback

from bot.worker import execute, logger
from util.logger import setup_logger

if __name__ == '__main__':
    setup_logger()
    while True:
        try:
            execute()
        except (KeyboardInterrupt, SystemExit):
            logger.error(traceback.format_exc())

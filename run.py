"""Module to run the bot. Executes the work() method of bot that executes the endless loop of reading comments and
submissions and replying to them if the match any response.
"""
from dotenv import load_dotenv

# Load env variables from `.env` file to be used by `os.environ.get()`
load_dotenv()

__author__ = 'MePsyDuck'

if __name__ == '__main__':
    from bot.worker import work, logger
    from util.logger import setup_logger

    setup_logger()
    try:
        work()
    except (KeyboardInterrupt, SystemExit):
        logger.error('Script stopped')
    except Exception as e:
        logger.error(e, exc_info=True)

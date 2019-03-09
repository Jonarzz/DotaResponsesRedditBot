import traceback

from bot.worker import execute, logger

if __name__ == '__main__':
    while True:
        try:
            execute()
        except (KeyboardInterrupt, SystemExit):
            logger.error(traceback.format_exc())

import logging
import os

import config

__author__ = 'MePsyDuck'

logger = logging.getLogger(config.BOT_LOG)


def setup_logger():
    """Method to setup loggers.
    Current logs only application logs and PRAW logs.

    Disabled file logging since Heroku does not offer persistent disk storage. All logs should be read from Stream
    Output instead.
    """

    if not os.path.exists(config.LOG_DIR):
        os.mkdir(config.LOG_DIR)

    log_format = config.LOG_FORMAT
    log_name = config.BOT_LOG
    log_formatter = logging.Formatter(log_format)
    log_level = logging.getLevelName(level=config.LOG_LEVEL)

    # Handlers
    info_log_file = os.path.join(config.LOG_DIR, config.INFO_FILENAME)
    info_file_handler = logging.FileHandler(info_log_file, mode='a')
    info_file_handler.setFormatter(log_formatter)
    info_file_handler.setLevel(logging.INFO)

    error_log_file = os.path.join(config.LOG_DIR, config.ERROR_FILENAME)
    error_file_handler = logging.FileHandler(error_log_file, mode='a')
    error_file_handler.setFormatter(log_formatter)
    error_file_handler.setLevel(logging.ERROR)

    praw_log_file = os.path.join(config.LOG_DIR, config.PRAW_FILENAME)
    praw_handler = logging.FileHandler(praw_log_file, mode='a')
    praw_handler.setLevel(logging.WARNING)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.DEBUG)

    # PRAW logging
    praw_logger = logging.getLogger(config.PRAW_LOG)
    praw_logger.setLevel(logging.WARNING)
    praw_logger.addHandler(stream_handler)
    praw_logger.addHandler(praw_handler)

    # Internal logging
    bot_logger = logging.getLogger(log_name)
    bot_logger.setLevel(log_level)
    bot_logger.addHandler(info_file_handler)  # This should be commented out if running on Heroku
    bot_logger.addHandler(error_file_handler)  # This should be commented out if running on Heroku
    bot_logger.addHandler(stream_handler)

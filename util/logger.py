"""Module to setup logging for bot and praw and provide logger for other modules.
"""

import logging
import os

from config import BOT_LOGGER, PRAW_LOGGER, LOG_DIR, LOG_FORMAT, LOG_LEVEL, INFO_FILENAME, ERROR_FILENAME, \
    PRAW_FILENAME, DEBUG, WARN_FILENAME

__author__ = 'MePsyDuck'

logger = logging.getLogger(BOT_LOGGER)


def setup_logger():
    """Method to setup loggers. Current logs only bot application logs and PRAW logs.

    Disable file logging is running on Heroku since Heroku does not offer persistent disk storage. All logs should be
    read from Stream output instead.
    """
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    log_formatter = logging.Formatter(LOG_FORMAT)
    log_level = logging.getLevelName(LOG_LEVEL)
    mode = 'w' if DEBUG else 'a'

    # Handlers
    info_log_file = os.path.join(LOG_DIR, INFO_FILENAME)
    info_file_handler = logging.FileHandler(info_log_file, mode=mode)
    info_file_handler.setFormatter(log_formatter)
    info_file_handler.setLevel(logging.INFO)

    warn_log_file = os.path.join(LOG_DIR, WARN_FILENAME)
    warn_file_handler = logging.FileHandler(warn_log_file, mode=mode)
    warn_file_handler.setFormatter(log_formatter)
    warn_file_handler.setLevel(logging.WARNING)

    error_log_file = os.path.join(LOG_DIR, ERROR_FILENAME)
    error_file_handler = logging.FileHandler(error_log_file, mode=mode)
    error_file_handler.setFormatter(log_formatter)
    error_file_handler.setLevel(logging.CRITICAL)

    praw_log_file = os.path.join(LOG_DIR, PRAW_FILENAME)
    praw_handler = logging.FileHandler(praw_log_file, mode=mode)
    praw_handler.setLevel(logging.WARNING)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.DEBUG)

    # PRAW logging
    praw_logger = logging.getLogger(PRAW_LOGGER)
    praw_logger.setLevel(log_level)
    praw_logger.addHandler(stream_handler)
    praw_logger.addHandler(praw_handler)

    # Internal logging
    bot_logger = logging.getLogger(BOT_LOGGER)
    bot_logger.setLevel(log_level)
    bot_logger.addHandler(info_file_handler)  # This should be commented out if running on Heroku
    bot_logger.addHandler(warn_file_handler)  # This should be commented out if running on Heroku
    bot_logger.addHandler(error_file_handler)  # This should be commented out if running on Heroku

    if DEBUG:
        bot_logger.addHandler(stream_handler)

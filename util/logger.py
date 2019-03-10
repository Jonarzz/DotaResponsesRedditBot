import logging
import os

import config


def setup_logger():
    """Method to setup loggers (Can also use a single logger for error and info messages).
    """

    if not os.path.exists(config.LOG_DIR):
        os.mkdir(config.LOG_DIR)

    # PRAW logging
    praw_log_file = os.path.join(config.LOG_DIR, config.PRAW_FILENAME)
    praw_handler = logging.FileHandler(praw_log_file, mode='a')
    praw_handler.setLevel(logging.DEBUG)
    praw_logger = logging.getLogger('prawcore')
    praw_logger.setLevel(logging.DEBUG)
    praw_logger.addHandler(praw_handler)

    # Internal logging
    log_format = '%(asctime)s %(funcName)-20s %(levelname)-8s %(message)s'
    log_name = ''
    info_log_file = os.path.join(config.LOG_DIR, config.INFO_FILENAME)
    error_log_file = os.path.join(config.LOG_DIR, config.ERROR_FILENAME)
    log_formatter = logging.Formatter(log_format)

    internal_logger = logging.getLogger(log_name)

    # uncomment this to get console output
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(log_formatter)
    # stream_handler.setLevel(logging.DEBUG)
    # internal_logger.addHandler(stream_handler)
    # praw_logger.addHandler(stream_handler)

    info_file_handler = logging.FileHandler(info_log_file, mode='a')
    info_file_handler.setFormatter(log_formatter)
    info_file_handler.setLevel(logging.INFO)
    internal_logger.addHandler(info_file_handler)

    error_file_handler = logging.FileHandler(error_log_file, mode='a')
    error_file_handler.setFormatter(log_formatter)
    error_file_handler.setLevel(logging.ERROR)
    internal_logger.addHandler(error_file_handler)

    internal_logger.setLevel(logging.INFO)
    return internal_logger


logger = setup_logger()

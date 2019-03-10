import logging
import os

import config


def setup_logger():
    """Method to setup loggers (Can also use a single logger for error and info messages).
    """

    if not os.path.exists(config.LOG_DIR):
        os.mkdir(config.LOG_DIR)

    log_format = '%(asctime)s %(funcName)-20s %(levelname)-8s %(message)s'
    log_name = ''
    log_file_info = os.path.join(config.LOG_DIR, config.INFO_FILENAME)
    log_file_error = os.path.join(config.LOG_DIR, config.ERROR_FILENAME)
    log_formatter = logging.Formatter(log_format)

    log = logging.getLogger(log_name)

    # uncomment this to get console output
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(log_formatter)
    # log.addHandler(stream_handler)

    file_handler_info = logging.FileHandler(log_file_info, mode='a')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(log_file_error, mode='a')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)
    return log


logger = setup_logger()

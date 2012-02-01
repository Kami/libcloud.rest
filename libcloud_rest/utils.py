import sys
import logging

__all__ = [
    'get_and_setup_logger'
]

LOG_FORMAT = '%(asctime)s %(levelname)s - %(message)s'

def get_and_setup_logger():
    logger = logging.getLogger('libcloud_rest.server')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.__stdout__)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

import logging


def get_logger():
    """
    init logger.
    """
    logger = logging.get_logger()
    logger.setLevel(logging.INFO)

    return logger

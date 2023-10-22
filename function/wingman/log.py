import logging


def get_logger():
    """
    init logger.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    return logger

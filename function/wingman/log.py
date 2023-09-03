import logging


def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    return logger

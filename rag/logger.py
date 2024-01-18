import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    # file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    # logging.getLogger().addHandler(file_handler)


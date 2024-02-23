import logging

from base.config import Config

file_handler = logging.FileHandler(Config.FILE_HANDLER)
stream_handler = logging.StreamHandler()


def configure_logging():
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)-s: %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=Config.LOG_LEVEL, handlers=[file_handler, stream_handler])

import logging

file_handler = logging.FileHandler("./process.log")
stream_handler = logging.StreamHandler()


def configure_logging():
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)-s: %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])

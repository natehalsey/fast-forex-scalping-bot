import logging
import multiprocessing

from multiprocessing import Process
from threading import Thread

logger = logging.getLogger(__name__)

multiprocessing.set_start_method("fork")


def create_thread(func, name=None, *args, **kwargs) -> Thread:
    logger.info("Creating new thread.")
    thread = Thread(target=func, name=name, args=args, kwargs=kwargs)

    thread.start()

    return thread


def create_process(func, name=None, *args, **kwargs) -> Process:
    logger.info(f"Starting new process.")
    proc = Process(target=func, name=name, args=args, kwargs=kwargs)

    proc.start()

    return proc

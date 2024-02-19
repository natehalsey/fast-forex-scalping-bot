import logging

from multiprocessing.connection import Listener

from core.controller import create_thread

logger = logging.getLogger(__name__)


def process_listener(sock_path, callback):
    while True:
        with Listener(sock_path, family="AF_UNIX") as listener:
            with listener.accept() as conn:
                logger.info("Connection accepted from", listener.last_accepted)
                callback(conn.recv_bytes())


def create_process_listener(sock_path, callback):
    create_thread(
        func=process_listener, name=f"{sock_path}.sock", kwargs={"callback": callback}
    )

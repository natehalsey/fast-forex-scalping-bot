import logging
import random
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from adapters.ibkr.connection_handler import ConnectionHandler
from core.controller import create_thread

logger = logging.getLogger(__name__)


def register_request():
    pass


class IBKRClient:
    def __init__(self):
        wrapper = EWrapper()
        self.client = EClient(wrapper)
        self.connection_handler = ConnectionHandler(self.client)

    @staticmethod
    def _generate_random_req_id():
        return random.randint(1, 10000)

    def _start_event_loop(self):
        while True:
            logger.info("Running inside client event loop ...")
            # wait for connections
            time.sleep(3)

    def start_client(self):
        create_thread(
            self.connection_handler.poll_client_connection,
            name="client_connection_handler",
        )
        self._start_event_loop()

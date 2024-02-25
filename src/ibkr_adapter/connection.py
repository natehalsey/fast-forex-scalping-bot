import logging
import time

from ibapi.client import EClient
from threading import Thread, Event

from ibkr_adapter.exceptions import NotConnectedError

logger = logging.getLogger(__name__)


class ConnectionHandler(Thread):
    def __init__(self, client, client_connected: Event):
        super().__init__()
        self.client: EClient = client
        self.client_connected = client_connected

    def _connect_to_client(self):
        if self.client.connState == EClient.CONNECTED:
            return

        logger.info("Connecting to IBKR API client ...")
        self.client.connect(host="ib-gateway", port=4002, clientId=0)

        if self.client.connState != EClient.CONNECTED:
            self.client_connected.clear()
            raise NotConnectedError("Failed to connect to client.")

        self.client_connected.set()
        logger.info("Connected to IBKR API client ...")

    def run(self):
        while True:
            try:
                self._connect_to_client()
            except NotConnectedError:
                self.client_connected.clear()
            time.sleep(1)

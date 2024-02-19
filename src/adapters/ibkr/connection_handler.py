import logging
import socket
import time

from ibapi.client import EClient

logger = logging.getLogger(__name__)


class ConnectionHandler:
    def __init__(self, client):
        self.client: EClient = client

    def _connect_to_client(self):
        # Check if we're already connected
        if self.client.connState == EClient.CONNECTED:
            return

        logger.info("Connecting to IBKR API client ...")
        self.client.connect("127.0.0.1", 4002, clientId=0)
        if self.client.connState != EClient.CONNECTED:
            raise socket.error  # same error caught by the connect class and smothered

    def _disconnect_from_client(self):
        logger.info("Disconnecting from IBKR API client ...")
        if self.client.connState == EClient.CONNECTED:
            self.client.disconnect()
        else:
            logger.info("Client not connected.")

    def connect(self):
        try:
            self._connect_to_client()
        except socket.error as e:
            logger.error("Failed to connect to client: %s", str(e))
            raise

    def poll_client_connection(self, delay=5):
        while True:
            try:
                self.connect()
            except Exception as e:  # pylint:disable=broad-exception-caught
                logger.error(
                    "Client not connected: %s, attempting to reconnect ...", str(e)
                )

            time.sleep(delay)

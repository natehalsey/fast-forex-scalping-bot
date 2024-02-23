import logging
import time
import queue

from dataclasses import dataclass
from ibapi.client import EClient
from threading import Thread, Event

from core.async_queue import AsyncQueue

logger = logging.getLogger(__name__)


@dataclass
class Response:
    response: str


class ResponseHandler(Thread):
    def __init__(
        self,
        client: EClient,
        response_queue: AsyncQueue,
    ):
        self.client: EClient = client
        super().__init__()
        self.response_queue: AsyncQueue = response_queue

        self.kill_response_handler: Event = Event()

    def run(self):
        while not self.kill_response_handler.is_set():
            try:
                response = self.client.msg_queue.get(block=True, timeout=0.2)
            except queue.Empty:
                time.sleep(1)
                continue

            self.response_queue.put(response)

    def kill(self):
        self.kill_response_handler.set()

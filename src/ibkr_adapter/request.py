import logging
import time
import queue

from dataclasses import dataclass
from ibapi.client import EClient
from threading import Thread, Event
from typing import Iterable, Any, Dict, List

from core.async_queue import AsyncQueue


logger = logging.getLogger(__name__)


@dataclass
class Request:
    request: str
    args: Iterable[Any]
    kwargs: Dict[str, Any]


class RequestHandler(Thread):
    REQUEST_QUEUE_TIME_MIN = 2
    REQUEST_QUEUE_TIME_MAX = 15
    MAX_THREADS = 4
    def __init__(
        self,
        client: EClient,
        request_queue: AsyncQueue[Request],
        client_connected: Event,
    ):
        self.client: EClient = client

        super().__init__()

        self.request_queue: AsyncQueue[Request] = request_queue
        self.client_connected: Event = client_connected
        self.kill_request_handler: Event = Event()

        request_worker = RequestWorker(self.client, self.request_queue, self.client_connected)
        request_worker.start()

        self.request_workers: List[RequestWorker] = [request_worker]

    def _scale_request_workers(self) -> None:
        """
        Some very basic request worker scaling based on oldest time in queue and whether we have any worker threads available to be used.
        """
        if len(self.request_workers) < self.MAX_THREADS and (
            self.request_queue.get_queue_time() > self.REQUEST_QUEUE_TIME_MAX
        ):
            request_worker = RequestWorker(
                self.client, self.request_queue, self.client_connected
            )
            request_worker.start()
            self.request_workers.append(request_worker)

        elif (len(self.request_workers) > 1) and (
            self.request_queue.get_queue_time() < self.REQUEST_QUEUE_TIME_MIN
        ):
            self.request_workers[0].kill()

    def _handle_request(self, request, *args, **kwargs) -> None:
        """
        Send a request over to a worker and unfortunately lose ownership until we see a response.
        """
        request = Request(request=request, args=args, kwargs=kwargs)
        self._scale_request_workers()
        self.request_queue.put(request)

    def run(self):
        """
        The main event loop, check if there's a message, if there is throw it to a worker.
        """
        while not self.kill_request_handler.is_set():
            try:
                request: Request = self.request_queue.get(
                    block=True, timeout=0.2
                )
                self._handle_request(request.request, *request.args, **request.kwargs)
            except queue.Empty:
                pass
            except Exception as e:
                logger.error("Request %s failed: %s", request.request, str(e))

        for request_worker in self.request_workers:
            request_worker.kill()

    def kill(self):
        self.kill_request_handler.set()

class RequestWorker(Thread):
    def __init__(
        self,
        client: EClient,
        request_queue: AsyncQueue[Request],
        client_connected: Event,
    ):
        self.client: EClient = client

        super().__init__()

        self.request_queue: AsyncQueue[Request] = request_queue
        self.client_connected: Event = client_connected

        self.kill_request_worker: Event = Event()

    def _request(self, request, *args, **kwargs) -> None:
        self.client_connected.wait()
        getattr(self.client, request)(*args, **kwargs)

    def run(self) -> None:
        while not self.kill_request_worker.is_set():
            try:
                request: Request = self.request_queue.get(block=True, timeout=0.2)
            except queue.Empty:
                time.sleep(1)
                continue
            try:
                self._request(request.request, *request.args, **request.kwargs)
            except Exception as e:
                logger.error("Request %s failed: %s", request.request, str(e))

    def kill(self):
        self.kill_request_worker.set()

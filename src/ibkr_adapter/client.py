import logging
import queue
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from multiprocessing import Process
from threading import Event

from ibkr_adapter.connection import ConnectionHandler
from ibkr_adapter.response import Response, ResponseHandler
from ibkr_adapter.request import Request, RequestHandler
from ibkr_adapter.wrapper import IBKRClientWrapper

from core.async_queue import AsyncQueue

logger = logging.getLogger(__name__)


class IBKRClient:
    def __init__(self):
        self.request_queue = AsyncQueue()
        self.response_queue = AsyncQueue()

        self.kill_client_process: Event = Event()

        self.client_process = IBKRClientProcess(
            self.request_queue, self.response_queue, self.kill_client_process
        )
        self.client_process.start()


    def get_account_value(self):
        request_summary = Request(
            request_id=1,
            request="reqAccountSummary",
            kwargs={"groupName": "All", "tags": "TotalCashValue"},
        )
        self.request_queue.put(request_summary)
        # while True:
        #     try:
        #         response: Response = self.response_queue.get()
        #     except queue.Empty:
        #         time.sleep(5)
        #         pass

        #     return response

        
        # cancel_summary = Request(
        #     request="cancellAccountSummary",
        #     kwargs={"reqId": request_summary.request_id},
        # )
        # self.request_queue.put(cancel_summary)

class IBKRClientProcess(Process):
    def __init__(
        self,
        request_queue: AsyncQueue,
        response_queue: AsyncQueue,
        kill_client_process: Event,
    ):
        super().__init__()

        self.request_queue: AsyncQueue = request_queue
        self.response_queue: AsyncQueue = response_queue

        wrapper = IBKRClientWrapper()
        self.client = EClient(wrapper=wrapper)

        self.client_connected: Event = Event()
        self.kill_client_process: Event = kill_client_process

    def run(self) -> None:
        # maintain a connecion
        connection_handler = ConnectionHandler(self.client, self.client_connected)
        connection_handler.start()

        # pool the request threads together
        request_handler = RequestHandler(
            self.client, self.request_queue, self.client_connected
        )
        request_handler.start()

        response_handler = ResponseHandler(self.client, self.response_queue)
        response_handler.start()

        # wait for kill client process event
        self.kill_client_process.wait()

        # request_handler.kill()
        # response_handler.kill()
        # connection_handler.kill()

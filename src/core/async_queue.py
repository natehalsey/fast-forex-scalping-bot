import time
import multiprocessing

from multiprocessing.queues import Queue

from typing import Any


class AsyncQueue(Queue):
    def __init__(self):
        ctx = multiprocessing.get_context()
        super(AsyncQueue, self).__init__(ctx=ctx)
        self.timestamps = []

    def put(self, obj: Any, block: bool = True, timeout: float | None = None):
        self.timestamps.append(time.time())
        super().put(obj, block, timeout)

    def get(self, block: bool = True, timeout: float | None = None):
        if len(self.timestamps) > 0:
            self.timestamps.pop(0)
        return super().get(block, timeout)

    def get_queue_time(self) -> int:
        if len(self.timestamps) > 0:
            return time.time() - self.timestamps[0]
        return 0

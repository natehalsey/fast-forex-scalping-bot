import logging
import time

from adapters.ibkr.client import IBKRClient
from core.controller import create_process

from base.logger import configure_logging

configure_logging()

logger = logging.getLogger(__name__)


def entry_point():
    # start process that ensures we have a continuous connection to the client
    # create_process_listener("/var/run/python-trading-bot", )

    client = IBKRClient()

    create_process(func=client.start_client, name="ibkr_client")

    while True:
        logger.info("Running inside main event loop ...")
        time.sleep(3)
    # # start process that continuously evaluates current positions
    # monitor = PositionMonitor(client)
    # finder = PositionFinder(client)

    # monitor.start_position_monitor()
    # finder.start_postion_finder()


if __name__ == "__main__":
    entry_point()

import logging
import time

from ibkr_adapter.client import IBKRClient

from base.logger import configure_logging

configure_logging()

logger = logging.getLogger(__name__)


def entry_point():
    logger.info("Starting IBKR Client ...")
    client = IBKRClient()

    while True:
        logger.info(client.get_account_value())
        time.sleep(10)

    # while True:
    #     time.sleep(10)


if __name__ == "__main__":
    entry_point()

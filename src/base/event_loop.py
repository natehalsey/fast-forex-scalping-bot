import asyncio
import logging
import signal
import sys

logger = logging.getLogger(__name__)


loop = asyncio.get_event_loop()
exit_flag = asyncio.Event()


def start_event_loop(event_name, callback):
    loop.create_task(callback)
    try:
        logger.info(f"Starting event loop for {event_name} ...")
        loop.run_forever()
    except Exception as e:
        logger.error(e, exc_info=True)
        pass
    finally:
        logger.info(f"Closing event loop for {event_name} ...")
        loop.close()


def _handle_sigterm(signum = None, frame = None):
    logger.info("Handlng SIGTERM, stopping event loop ...")
    loop.stop()

signal.signal(signal.SIGTERM, _handle_sigterm)

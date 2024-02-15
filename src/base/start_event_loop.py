import asyncio
import logging

from src.base.logger import configure_logging

configure_logging()

logger = logging.getLogger(__name__)
exit_flag = asyncio.Event()

loop = asyncio.get_event_loop()

async def startup():
    logger.info("Starting.")

async def shutdown():
    logger.info("Stopping.")

def start_event_loop():

    logger.info("Starting event loop.")
    loop.create_task(startup())

    try:
        loop.run_forever()
    except Exception as e:
        logger.error(e, exc_info=True)
        pass
    finally:
        logger.info("Stopping event loop.")
        loop.close()

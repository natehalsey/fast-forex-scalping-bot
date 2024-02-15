import logging

from base.event_loop import start_event_loop
from base.logger import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

PYTHON_TRADING_BOT_MAIN_EVENT_LOOP="python-trading-bot"

async def _python_bot_entry():
    logger.info("hello python bots")

if __name__ == "__main__":
    start_event_loop(PYTHON_TRADING_BOT_MAIN_EVENT_LOOP, _python_bot_entry())

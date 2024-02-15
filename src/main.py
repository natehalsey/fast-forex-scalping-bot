import daemon
import logging
from src.base.start_event_loop import start_event_loop
#from src.base.logger import get_handlers

logger = logging.getLogger(__name__)

def start_daemon():
    logger.info("Starting daemon.")
    # TODO: Set PID file to kill daemon
    with daemon.DaemonContext(   
        files_preserve = [3,4],
        detach_process=True
        
   ):
        start_event_loop()
    #logger.info("Outside daemon.")

def stop_daemon():
    logger.info("Stopping daemon.") 

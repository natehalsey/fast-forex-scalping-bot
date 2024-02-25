import logging

from ibapi.wrapper import EWrapper
from ibapi.utils import current_fn_name

logger = logging.getLogger(__name__)

class IBKRClientWrapper(EWrapper):
    def __init__(self):
        super().__init__()

        self.next_valid_req_id: int = None
        self.total_cash_value: float = None
    
    def accountSummaryEnd(self, reqId: int):
        #return super().accountSummaryEnd(reqId)
        self.client.cancelAccountSummary(reqId)
    
    def updateAccountValue(self, reqId: int, account: str, tag:str, value:str, currency: str):
        logger.info("%s, %s", current_fn_name(), vars())
        
    def nextValidId(self, orderId: int):
        self.next_valid_req_id = orderId

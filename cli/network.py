from .testnet import *

DEFAULT_CONNECT_TIMEOUT_SECS: float = 5.0
DEFAULT_TIMEOUT_SECS: float = 30.0
DEFAULT_MAX_RETRIES: int = 15
DEFAULT_RETRY_DELAY: float = 0.2
DEFAULT_WAIT_FOR_TRANSACTION_TIMEOUT_SECS: float = 30.0
DEFAULT_WAIT_FOR_TRANSACTION_WAIT_DURATION_SECS: float = 0.2

class StaleResponseError(Exception):
    pass

class InvalidMethodError(Exception):
    pass

'''eth'''
class InvalidTokenError(Exception):
    pass


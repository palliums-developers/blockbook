import requests
import typing
from cli.util import Retry
from cli.network import *

class Client:
    def __init__(
        self,
        session: typing.Optional[requests.Session] = None,
        timeout: typing.Optional[typing.Tuple[float, float]] = None,
        retry: typing.Optional[Retry] = None,
    ):
        self._session = session or requests.Session()
        self._timeout = timeout or (DEFAULT_CONNECT_TIMEOUT_SECS, DEFAULT_TIMEOUT_SECS)
        self._retry = retry or Retry(DEFAULT_MAX_RETRIES, DEFAULT_RETRY_DELAY, StaleResponseError)
        self._method_to_urls = btc_method_to_urls

    def get_transaction(self, txid):
        return self.execute("tx", [txid])

    def get_account_info(self, addr):
        return self.execute("address", [addr])

    def get_balance(self, addr):
        ac = self.get_account_info(addr)
        return ac.get("balance")

    def get_utxo(self, addr):
        return self.execute("utxo", [addr])

    def send_transction(self, tx):
        return self.execute("sendtx", [tx])

    def estimate_fee(self, block_height):
        return self.execute("estimatefee", [block_height])

    def execute(self, method, params):
        return self._retry.execute(
            lambda: self.execute_without_retry(method, params)
        )

    def execute_without_retry(self, method, params):
        url = self._method_to_urls.get(method)
        if url is None:
            raise InvalidMethodError(f"{method} is not valid method")
        for param in params:
            url += str(param)
        return self.get(url)

    def get(self, url):
        response = self._session.get(url, timeout=self._timeout)
        response.raise_for_status()
        return response.json()


def test():
    client = Client()
    print(client.get_transaction("76dd6c1519b87deaf123247afc70afb5eede42dbdb57d3738693a92b86138d97"))
    print(client.get_account_info("2N4YXTxKEso3yeYXNn5h42Vqu3FzTTQ8Lq5"))
    print(client.get_utxo("2N4YXTxKEso3yeYXNn5h42Vqu3FzTTQ8Lq5"))
    print(client.estimate_fee(1))

if __name__ == "__main__":
    test()
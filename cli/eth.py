import json
from web3 import Web3
from cli.network import *

class Client:
    def __init__(self):
        self._w3 = Web3(Web3.HTTPProvider(eth_url_prefix))

    def get_balance(self, addr):
        return self._w3.eth.get_balance(addr)

    def get_erc20_balance(self, addr, token):
        token = token.lower()
        self.assert_token_exist(token) 
        token_addr, abi = tokens.get(token)
        token_addr = self._w3.toChecksumAddress(token_addr)
        contract = self._w3.eth.contract(token_addr, abi=abi)
        return contract.functions.balanceOf(addr).call()

    def send_raw_transaction(self, raw_transaction):
        self._w3.eth.send_raw_transaction(raw_transaction)

    def assert_token_exist(self, token):
        if tokens.get(token) is None:
            raise InvalidTokenError(f"token:{token} not exist")

if __name__ == "__main__":
    client = Client()
    print(client.get_account("0x617DA121aBf03D4c1AF572F5a4E313E26BeF7BDc"))

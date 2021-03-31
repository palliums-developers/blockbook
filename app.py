from flask import Flask

from cli.eth import Client as EClient
from cli.btc import Client as BClient

app = Flask(__name__)

version = "v1"
def version_prefix(uri):
    return f"/{version}{uri}"

def eth_prefix(uri):
    return version_prefix("/eth" + uri)

def make_response(data=None, status=None, message=None):
    status = status or 200
    message = message or "success"

    return {
        "status": status,
        "data": data,
        "message": message
    }

def btc_prefix(uri):
    return version_prefix("/btc" + uri)

def gen_cli(chain):
    if chain == "eth":
        return EClient()
    if chain == "btc":
        return BClient()

@app.route(eth_prefix("/balance/<token>/<addr>"))
def eth_get_balance(token, addr):
    cli = gen_cli("eth")
    token = token.lower()
    if token == "eth":
        return cli.get_balance(addr)
    return cli.get_erc20_balance(addr, token)

@app.route(eth_prefix("/sendtx/tx"))
def eth_send_raw_transaction(tx):
    cli = gen_cli("eth")
    return cli.send_raw_transaction(tx)

@app.route(btc_prefix("/balance/<addr>"))
def btc_get_balance(addr):
    cli = gen_cli("btc")
    return cli.get_balance(addr)

@app.route(btc_prefix("/<addr>"))
def btc_get_account_info(addr):
    cli = gen_cli("btc")
    return cli.get_account_info(addr)

@app.route(btc_prefix("/utxo/<addr>"))
def btc_get_utxos(addr):
    cli = gen_cli("btc")
    return cli.get_utxo(addr)

@app.route(btc_prefix("/estimate_fee"))
def btc_estimate_fee():
    cli = gen_cli("btc")
    return cli.estimate_fee(1)

@app.route(btc_prefix("/sendtx/<tx>"))
def btc_send_tx(tx):
    cli = gen_cli("btc")
    return cli.send_raw_transaction(tx)

@app.errorhandler(Exception)
def handle_exception(e):
    return make_response(status=600, message=str(e))

if __name__ == '__main__':
    app.run(port=10001, debug=True)
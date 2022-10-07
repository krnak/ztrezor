from requests import get, post


def call(method, name, *args, **kwargs):
    print(f"call api.{name}")
    res = method(
        f"https://sochain.com/api/v2/{name}/ZECTEST/{'/'.join(args)}",
        data=kwargs,
    ).json()
    if res["status"] != "success":
        raise ValueError(str(res["data"]))
    else:
        return res["data"]


def send_tx(tx_hex):
    txid = call(post, "send_tx", tx_hex=tx_hex)["txid"]
    print(f"https://sochain.com/tx/ZECTEST/{txid}")
    return txid


def is_tx_confirmed(txid):
    return call(get, "is_tx_confirmed", txid)["is_confirmed"]


def get_tx_outputs(txid):
    return call(get, "get_tx_outputs", txid)["outputs"]


def get_tx_unspent(address):
    return call(get, "get_tx_unspent", address)["txs"]

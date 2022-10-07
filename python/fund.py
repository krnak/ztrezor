import requests
import time
import json
import subprocess
from datetime import datetime
import os

from common import *
import cases
from tx import Tx
from py_trezor_orchard import *
import api
import getcmxs

from trezorlib.messages import (
    TxInputType, TxOutputType, OutputScriptType,
    ZcashSignatureType as SigType,
    ZcashOrchardInput, InputScriptType
)
from trezorlib.client import get_default_client
from trezorlib import btc, messages, zcash
from trezorlib.exceptions import TrezorFailure
from trezorlib.tools import parse_path

import random


def gen_funding(required):
    res = get_resources()
    required_total = sum(f[1] for f in required) + FEE
    funding = []
    foo = list(res.items())
    random.shuffle(foo)
    for k, v in foo:
        if not k[0].startswith("m/44h"):
            continue
        funding.append(k)
        required_total -= k[1]
        if required_total <= 0:
            break

    assert required_total <= 0

    tx = cases.Transaction(
        name=f"funding_{random.randint(1000, 9999)}",
        outputs=list(map(funding_to_output, required)),
        funding=funding,
    )

    tx.fund(res, add_change=True)
    return tx


def sync_cmxs():
    print("sync cmxs")
    new_cmxs = getcmxs.sync()
    print(f"{len(new_cmxs)} synced")


def update_paths():
    print("update paths")
    subprocess.run(['/home/agi/code/ztrezor/client/target/debug/client'])


def get_resources():
    resources = dict()

    for cmx_file in os.listdir("/home/agi/code/ztrezor/notes"):
        cmx = cmx_file.split(".")[0]
        o_input = load_note(cmx)
        key = (f"m/32h/1h/{o_input[3]}h", o_input[0].value)
        if key not in resources:
            resources[key] = []
        if o_input[1][0] != 0:  # if has witness
            resources[key].append(o_input[:-1])

    for txo in api.get_tx_unspent("tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu"):
        amount = int(float(txo["value"]) * ZEC)
        key = ("m/44h/1h/0h/0/0", amount)
        if key not in resources:
            resources[key] = []
        resources[key].append(
            TxInputType(
                address_n=parse_path("m/44h/1h/0h/0/0"),
                amount=amount,
                prev_hash=bytes.fromhex(txo["txid"]),
                prev_index=txo["output_no"],
                script_type={
                    "76a914a579388225827d9f2fe9014add644487808c695d88ac": InputScriptType.SPENDADDRESS,
                    #"scripthash": InputScriptType.PAYTOSCRIPTHASH,
                }[txo["script_hex"]],
            )
        )

    return resources


def merge_rendered():
    file = open("/home/agi/code/ztrezor/rendered/all.py", "w")
    for filename in os.listdir("/home/agi/code/ztrezor/rendered"):
        if not filename.startswith("funding") and filename != "all.py":
            with open(f"/home/agi/code/ztrezor/rendered/{filename}") as f:
                file.write(f.read())
                file.write("\n\n")
    file.close()

def load(name):
    return Tx.load(name)

def from_the_beginning():
    txs = cases.CASES
    txs = [Tx.load(x.name) for x in cases.CASES]
    """
    required = [f for tx in txs for f in tx.funding]
    ftx = gen_funding(required)
    ftx.sign()
    ftx.prove()
    ftx.send()
    ftx.wait_for()
    time.sleep(10)
    """
    sync_cmxs()
    update_paths()
    res = get_resources()
    for tx in txs:
        tx.fund(res)
    for tx in txs:
        tx.sign()
    for tx in txs:
        tx.prove()
    for tx in txs:
        tx.send()
    for tx in txs:
        tx.render()


if __name__ == "__main__":
    txs = [cases.Transaction.load(x.name) for x in cases.CASES]
    for tx in txs:
        tx.render()
    merge_rendered()
    #from_the_beginning()
    """
    for tx in map(cases.Transaction.load, ("t2z", "z2z", "z2t")):
        tx.sign()
        tx.prove()
        tx.send()
        tx.render()
    """

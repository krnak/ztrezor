import requests
import time
import json
import subprocess
from datetime import datetime
import os
from pprint import pprint
from common import *
from cases import CASES
from tx import Tx
from py_trezor_orchard import *
import api
import getcmxs
import zingo
from tx_inputs import TInput, OInput

from trezorlib.messages import (
    TxInputType, TxOutputType, OutputScriptType,
    ZcashSignatureType as SigType,
    ZcashOrchardInput, InputScriptType, ZcashOrchardOutput
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
        funding.append(k)
        required_total -= k[1]
        if required_total <= 0:
            break

    assert required_total <= 0

    tx = Tx(
        name=f"funding_{random.randint(1000, 9999)}",
        outputs=list(map(funding_to_output, required)),
        funding=funding,
    )

    tx.fund(res, add_change=True)
    return tx

def get_resources():
    utxos = zingo.notes()
    resources = {}
    for note in utxos["unspent_orchard_notes"]:
        o_input = OInput(
            note={
                "recipient": bytes.fromhex(note["note_recipient"]),
                "value": note["value"],
                "rho": bytes.fromhex(note["note_rho"]),
                "rseed": bytes.fromhex(note["note_rseed"]),
            },
            account=0,
            witness=(
                note["merkle_tree_position"],
                list(map(bytes.fromhex, note["merkle_tree_path"]))
            ),
            anchor=bytes.fromhex(note["merkle_tree_root"]),
            cmx=note["note_cmx"],
        )
        key = (o_input.path(), o_input.value())
        if key not in resources:
            resources[key] = []
        resources[key].append(o_input)

    for utxo in utxos["utxos"]:
        t_input = TInput(inner=TxInputType(
            address_n=parse_path("m/44h/1h/0h/0/0"),  # TODO
            amount=utxo["value"],
            prev_hash=bytes.fromhex(utxo["created_in_txid"]),
            prev_index=utxo["output_index"],
            script_type=InputScriptType.SPENDADDRESS,
        ))
        key = (t_input.path(), t_input.value())
        if key not in resources:
            resources[key] = []
        resources[key].append(t_input)

    return resources
    #return {**get_utxos(), **get_utxns()}


def merge_rendered():
    file = open("/home/agi/gh/jarys/ztrezor/rendered/all.py", "w")
    for filename in os.listdir("/home/agi/gh/jarys/ztrezor/rendered"):
        if not filename.startswith("funding") and filename != "all.py":
            with open(f"/home/agi/gh/jarys/ztrezor/rendered/{filename}") as f:
                file.write(f.read())
                file.write("\n\n")
    file.close()

def load(name):
    return Tx.load(name)

def from_the_beginning():
    # txs = cases.CASES
    # txs = [Tx.load(x.name) for x in cases.CASES_2]
    # required = [f for tx in txs for f in tx.funding]
    # tx = gen_funding(required)
    #return
    #ftx = gen_funding(required)
    #ftx.sign()
    #ftx.prove()
    #ftx.send()
    #ftx = load("funding_3862")
    #ftx.prove()
    #ftx.send()
    #time.sleep(10)
    #sync_cmxs()
    #update_paths()
    #"""
    #res = get_resources()
    #for tx in CASES:
    #    tx.fund(res)
    #for tx in CASES:
    #    tx.sign()
    #for tx in CASES:
    #    tx.prove()
    #for tx in CASES:
    #    tx.send()
    for tx in CASES:
        tx.render()
    #"""

if __name__ == "__main__":
    # pprint(get_resources())
    from_the_beginning()
    # tx = gen_funding([("m/32h/1h/0h", 42000)])
    #tx = Tx.load("funding_3570")
    # print(tx)
    # tx.prove()
    """
    txs = [Tx.load(x.name) for x in cases.CASES]
    for tx in txs:
        tx.expected = "gen"
        tx.gen_expected()
        tx.render()
    merge_rendered()
    #from_the_beginning()
    for tx in map(cases.Transaction.load, ("t2z", "z2z", "z2t")):
        tx.sign()
        tx.prove()
        tx.send()
        tx.render()
    """

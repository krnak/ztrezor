import requests
import time
import json
import subprocess
from datetime import datetime
import os

from common import *
import cases
from py_trezor_orchard import *
import api
import getcmxs

from trezorlib.messages import (
    TxInputType, TxOutputType, OutputScriptType,
    ZcashSignatureType as SigType,
    ZcashOrchardInput,
)
from trezorlib.client import get_default_client
from trezorlib import btc, messages, zcash
from trezorlib.exceptions import TrezorFailure
from trezorlib.tools import parse_path

client = get_default_client()

if True:
    funding_inputs = api.get_tx_unspent("tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu")
    print("choose funding utxo:")
    possibilities = []
    f_max = 0
    default = None
    for i, utxo in enumerate(funding_inputs):
        f_txid = utxo["txid"]
        f_amount = int(float(utxo["value"]) * ZEC)
        f_index = utxo["output_no"]
        if f_max < f_amount:
            f_max = f_amount
            default = i
        date = datetime.fromtimestamp(utxo["time"])
        print(f"{i: 2d}. {date.date()} {f_txid[:6]}:{f_index} {utxo['value']} TAZ")
        possibilities.append((f_amount, f_txid, f_index))

    idx = input(f"[default={default}]:")
    if idx:
        idx = int(idx)
    else:
        idx = default

    f_amount, f_txid, f_index = possibilities[idx]

    t_outputs = list(cases.required_utxos())
    o_outputs = list(cases.required_utxns())
    total_out = sum(txi.amount for txi in t_outputs + o_outputs)
    t_outputs.append(  # change
        TxOutputType(
            address_n=parse_path("m/44h/1h/0h/0/0"),
            amount=f_amount - total_out - FEE,
            script_type=OutputScriptType.PAYTOADDRESS,
        )
    )

    protocol = zcash.sign_tx(
        client,
        t_inputs=[
            TxInputType(
                address_n=parse_path("m/44h/1h/0h/0/0"),
                amount=f_amount,
                prev_hash=bytes.fromhex(f_txid),
                prev_index=f_index,
            ),
        ],
        t_outputs=t_outputs,
        o_inputs=[],
        o_outputs=o_outputs,
        coin_name="Zcash Testnet",
        verbose=True,
    )

    shielding_seed = next(protocol)
    sighash = next(protocol)
    signatures, serialized_tx = next(protocol)

    builder = TrezorBuilder(
        [],
        [OrchardOutput(txo) for txo in o_outputs],
        zcash.EMPTY_ANCHOR,
        fvk,
        shielding_seed,
    )

    bundle = builder.build()
    bundle.prepare(sighash)
    print("proving")
    bundle.create_proof(pk())
    print("proving finished")
    bundle.finalize()

    print("save notes:")
    for note, cmx in bundle.decrypt_outputs_with_fvk(fvk):
        cmx = bytes(cmx).hex()
        print(f"- {cmx}")
        with open(f"/home/agi/code/ztrezor/notes/{cmx}.json", "w") as f:
            json.dump(note, f)
        with open(f"/home/agi/code/ztrezor/witnesses/{cmx}.json", "w") as f:
            f.write("[]")
    print()

    tx = serialized_tx[:-1] + bytes(bundle.serialized())

    print("save tx to ~/tx")
    with open("/home/agi/tx", "w") as f:
        f.write(tx.hex())

if True:
    txid_new = api.send_tx(tx_hex=tx.hex())
    print("funding txid:", txid_new)
    print(f"https://sochain.com/tx/ZECTEST/{txid_new}")
else:
    txid_new = "2b3054f5ee4b00371cfa9ebf7d2853a54b0d17e03bedd4c268e0fdc6cb7b0abc"
    print("txid set manually")

if True:
    while True:
        if api.is_tx_confirmed(txid_new):
            print("confirmed")
            break
        else:
            print("waiting for confirmation")
            time.sleep(30)


if True:
    print("wait for zcashd")
    time.sleep(2)
    print("sync cmxs")
    new_cmxs = getcmxs.sync()
    print(f"{len(new_cmxs)} synced")

    print("compute paths")
    subprocess.run(['/home/agi/code/ztrezor/client/target/debug/client'])

if True:
    with open("/home/agi/code/ztrezor/witnesses/anchor") as f:
        anchor_hex = f.read()
        print(f"anchor: {anchor_hex}")
        anchor = bytes.fromhex(anchor_hex)

    sources = dict()

    for cmx_file in os.listdir("/home/agi/code/ztrezor/notes"):
        cmx = cmx_file.split(".")[0]
        o_input = load_note(cmx)
        key = ("m/32h/1h/0h", o_input[0].value)
        if key not in sources:
            sources[key] = []
        sources[key].append(o_input)

    for txo in api.get_tx_outputs(txid_new):
        amount = int(float(txo["value"]) * ZEC)
        key = ("m/44h/1h/0h/0/0", amount)
        if key not in sources:
            sources[key] = []
        sources[key].append(
            TxInputType(
                address_n=parse_path("m/44h/1h/0h/0/0"),
                amount=amount,
                prev_hash=bytes.fromhex(txid_new),
                prev_index=txo["output_no"],
            )
        )

    txids = []
    for case in cases.CASES:
        txid = case.send(client, sources, anchor)
        txids.append(txid)

    while True:
        if all(api.is_tx_confirmed(x) for x in txids):
            print("confirmed")
            break
        else:
            print("waiting for confirmations")
            time.sleep(20)

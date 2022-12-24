import json
import yaml
import os

from trezorlib.tools import parse_path
from trezorlib.messages import (
    OutputScriptType, ZcashOrchardOutput, TxOutputType, TxInputType, ZcashOrchardInput
)
import tx_inputs

from trezorlib.client import get_default_client
from py_trezor_orchard import ProvingKey

H = 1 << 31
ZEC = 10**8
FEE = int(0.0001 * ZEC)
BASE = int(0.01 * ZEC)

fvk = bytes.fromhex("d38d537a1195343afb128a58958f2cba8f6435488fa57e1a09c23451a07d7a14ca39d4b3d4163372065a1e54a4bc33d17f441f913ef91cda6e76c265fac32529d72fc9967f7751a5c8abc2b0b677879faef25871156faf6726ee79a7b4d5a00b")

PK = None
CLIENT = None


def get_client():
    global CLIENT
    if CLIENT is None:
        CLIENT = get_default_client()
    return CLIENT


def pk():
    global PK
    if PK is None:
        print("building proving key")
        PK = ProvingKey.build()
        print("proving key built")
    return PK


PATH_TO_ADDRESS = {
    "m/44h/1h/0h/0/0": "tmQoJ3PTXgQLaRRZZYT6xk8XtjRbr2kCqwu",
    "m/32h/1h/0h": "utest1gu6rg6hse8v0pd7mhgfn80v5vvdhuwn30wztyrczxsyj46ngpp2ryw36az6vlmlle8xns5k6pdlkgycr27naa2hpn3wspuvsxv0yzz62",
    "m/32h/1h/2h": "utest1d5kpwc69vplme7sae0rjmc88599xxy03767yzpplessv72p3pf3e023lkhs8zxdxw3slvnj4xaf0u3sqp9qe7qf0vq0fcc2jpcr87cks",
}


def funding_to_output(f):
    amount = f[1]
    if f[0].startswith("m/44h"):
        return TxOutputType(
            address=PATH_TO_ADDRESS.get(f[0]),
            amount=amount,
            script_type=OutputScriptType.PAYTOADDRESS,
        )
    elif f[0].startswith("m/32h"):
        return ZcashOrchardOutput(
            address=PATH_TO_ADDRESS.get(f[0]),
            amount=amount,
        )
    elif f[0].startswith("t"):
        return TxOutputType(
            address=f[0],
            amount=amount,
            script_type=OutputScriptType.PAYTOADDRESS,
        )
    elif f[0].startswith("u"):
        return ZcashOrchardOutput(
            address=f[1],
            amount=amount,
        )
    else:
        raise ValueError


def get_anchor():
    with open("/home/agi/code/ztrezor/witnesses/anchor") as f:
        anchor_hex = f.read()
        print(f"anchor: {anchor_hex}")
        anchor = bytes.fromhex(anchor_hex)
    return anchor

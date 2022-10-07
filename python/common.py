import json
import yaml
import os

from trezorlib.tools import parse_path
from trezorlib.messages import (
    OutputScriptType, ZcashOrchardOutput, TxOutputType, TxInputType, ZcashOrchardInput
)

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


def create_note(cmx, note, account):
    print(f"saving note {cmx}")
    with open(f"/home/agi/code/ztrezor/notes/{cmx}.yaml", "w") as f:
        f.write(yaml.dump((note, account)))
    with open(f"/home/agi/code/ztrezor/witnesses/{cmx}.json", "w") as f:
        f.write("[0,[]]")


def load_note(cmx):
    print(f"loading note {cmx}")
    with open(f"/home/agi/code/ztrezor/notes/{cmx}.yaml", "r") as f:
        note, account = yaml.load(f.read(), Loader=yaml.Loader)
    with open(f"/home/agi/code/ztrezor/witnesses/{cmx}.json", "r") as f:
        pos, path = json.load(f)

    path = list(map(bytes.fromhex, path))
    input = ZcashOrchardInput(**note)
    return input, (pos, path), cmx, account


def spend_note(cmx):
    print(f"spend note {cmx}")
    try:
        os.rename(f"/home/agi/code/ztrezor/notes/{cmx}.yaml", f"/home/agi/code/ztrezor/spent_notes/{cmx}.yaml")
        os.remove(f"/home/agi/code/ztrezor/witnesses/{cmx}.json")
    except FileNotFoundError:
        pass


def funding_to_output(f):
    amount = f[1]
    if f[0].startswith("m/44h"):
        return TxOutputType(
            address_n=parse_path(f[0]),
            amount=amount,
            script_type=OutputScriptType.PAYTOADDRESS,
        )
    elif f[0].startswith("t"):
        return TxOutputType(
            address=f[0],
            amount=amount,
            script_type=OutputScriptType.PAYTOADDRESS,
        )
    elif f[0].startswith("m/32h"):
        return ZcashOrchardOutput(
            amount=amount,
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
